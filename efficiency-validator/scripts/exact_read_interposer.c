/*
 * macOS user-space read interposer for exact-read-1.
 *
 * The interposer records bytes returned by read/pread/readv/preadv and a
 * version snapshot taken at first open. It deliberately emits a hard gap for
 * mmap and writes because those access patterns cannot be reconstructed as
 * exact returned bytes by this adapter.
 */

#define _DARWIN_C_SOURCE

#include <CommonCrypto/CommonDigest.h>
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <libgen.h>
#include <limits.h>
#include <pthread.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>

typedef int (*open_fn)(const char *, int, ...);
typedef int (*openat_fn)(int, const char *, int, ...);
typedef int (*close_fn)(int);
typedef ssize_t (*read_fn)(int, void *, size_t);
typedef ssize_t (*pread_fn)(int, void *, size_t, off_t);
typedef ssize_t (*readv_fn)(int, const struct iovec *, int);
typedef ssize_t (*preadv_fn)(int, const struct iovec *, int, off_t);
typedef off_t (*lseek_fn)(int, off_t, int);
typedef int (*fstat_fn)(int, struct stat *);
typedef int (*fcntl_fn)(int, int, ...);
typedef void *(*mmap_fn)(void *, size_t, int, int, int, off_t);
typedef int (*munmap_fn)(void *, size_t);
typedef ssize_t (*write_fn)(int, const void *, size_t);
typedef ssize_t (*pwrite_fn)(int, const void *, size_t, off_t);
typedef ssize_t (*writev_fn)(int, const struct iovec *, int);
typedef int (*dup_fn)(int);
typedef int (*dup2_fn)(int, int);

static open_fn real_open;
static openat_fn real_openat;
static close_fn real_close;
static read_fn real_read;
static pread_fn real_pread;
static readv_fn real_readv;
static preadv_fn real_preadv;
static lseek_fn real_lseek;
static fstat_fn real_fstat;
static fcntl_fn real_fcntl;
static mmap_fn real_mmap;
static munmap_fn real_munmap;
static write_fn real_write;
static pwrite_fn real_pwrite;
static writev_fn real_writev;
static dup_fn real_dup;
static dup2_fn real_dup2;

static pthread_once_t resolve_once = PTHREAD_ONCE_INIT;
static pthread_mutex_t state_lock = PTHREAD_MUTEX_INITIALIZER;
static int log_fd = -1;
static unsigned long event_index;
static const char *run_id;
static const char *case_id;
static const char *trace_id;

struct fd_entry {
    int fd;
    char *path;
    int readable;
    struct fd_entry *next;
};

struct snapshot_entry {
    char *path;
    char hash[65];
    struct snapshot_entry *next;
};

static struct fd_entry *fd_entries;
static struct snapshot_entry *snapshots;

static void resolve_symbols(void) {
    real_open = (open_fn)dlsym(RTLD_NEXT, "open");
    real_openat = (openat_fn)dlsym(RTLD_NEXT, "openat");
    real_close = (close_fn)dlsym(RTLD_NEXT, "close");
    real_read = (read_fn)dlsym(RTLD_NEXT, "read");
    real_pread = (pread_fn)dlsym(RTLD_NEXT, "pread");
    real_readv = (readv_fn)dlsym(RTLD_NEXT, "readv");
    real_preadv = (preadv_fn)dlsym(RTLD_NEXT, "preadv");
    real_lseek = (lseek_fn)dlsym(RTLD_NEXT, "lseek");
    real_fstat = (fstat_fn)dlsym(RTLD_NEXT, "fstat");
    real_fcntl = (fcntl_fn)dlsym(RTLD_NEXT, "fcntl");
    real_mmap = (mmap_fn)dlsym(RTLD_NEXT, "mmap");
    real_munmap = (munmap_fn)dlsym(RTLD_NEXT, "munmap");
    real_write = (write_fn)dlsym(RTLD_NEXT, "write");
    real_pwrite = (pwrite_fn)dlsym(RTLD_NEXT, "pwrite");
    real_writev = (writev_fn)dlsym(RTLD_NEXT, "writev");
    real_dup = (dup_fn)dlsym(RTLD_NEXT, "dup");
    real_dup2 = (dup2_fn)dlsym(RTLD_NEXT, "dup2");
}

static void ensure_symbols(void) {
    pthread_once(&resolve_once, resolve_symbols);
}

static void json_string(const char *value, char *out, size_t capacity) {
    size_t cursor = 0;
    if (capacity == 0) return;
    out[cursor++] = '"';
    for (const unsigned char *p = (const unsigned char *)value; *p && cursor + 2 < capacity; p++) {
        unsigned char c = *p;
        if (c == '"' || c == '\\') {
            if (cursor + 2 >= capacity) break;
            out[cursor++] = '\\';
            out[cursor++] = (char)c;
        } else if (c == '\n' || c == '\r' || c == '\t') {
            if (cursor + 2 >= capacity) break;
            out[cursor++] = '\\';
            out[cursor++] = c == '\n' ? 'n' : c == '\r' ? 'r' : 't';
        } else if (c < 0x20) {
            if (cursor + 6 >= capacity) break;
            cursor += (size_t)snprintf(out + cursor, capacity - cursor, "\\u%04x", c);
        } else {
            out[cursor++] = (char)c;
        }
    }
    if (cursor + 2 <= capacity) {
        out[cursor++] = '"';
        out[cursor] = '\0';
    } else {
        out[capacity - 1] = '\0';
    }
}

static char *base64_encode(const unsigned char *data, size_t length) {
    static const char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    size_t output_length = ((length + 2) / 3) * 4;
    char *output = (char *)malloc(output_length + 1);
    if (output == NULL) return NULL;
    size_t i = 0;
    size_t j = 0;
    while (i < length) {
        uint32_t octet_a = data[i++];
        bool has_b = i < length;
        uint32_t octet_b = has_b ? data[i++] : 0;
        bool has_c = i < length;
        uint32_t octet_c = has_c ? data[i++] : 0;
        uint32_t triple = (octet_a << 16) | (octet_b << 8) | octet_c;
        output[j++] = alphabet[(triple >> 18) & 0x3f];
        output[j++] = alphabet[(triple >> 12) & 0x3f];
        output[j++] = has_b ? alphabet[(triple >> 6) & 0x3f] : '=';
        output[j++] = has_c ? alphabet[triple & 0x3f] : '=';
    }
    output[j] = '\0';
    return output;
}

static void sha256_hex(const unsigned char *data, size_t length, char output[65]) {
    unsigned char digest[CC_SHA256_DIGEST_LENGTH];
    CC_SHA256(data, (CC_LONG)length, digest);
    for (size_t i = 0; i < sizeof(digest); i++) {
        snprintf(output + (i * 2), 3, "%02x", digest[i]);
    }
    output[64] = '\0';
}

static void emit_json(const char *json) {
    if (log_fd < 0 || json == NULL) return;
    size_t length = strlen(json);
    if (real_write != NULL) {
        (void)real_write(log_fd, json, length);
        (void)real_write(log_fd, "\n", 1);
    }
}

static const char *program_name(void) {
    const char *name = getprogname();
    return name == NULL ? "unknown" : name;
}

static void emit_started(void) {
    char run[512], case_value[512], trace[512], process[512], line[2400];
    json_string(run_id == NULL ? "" : run_id, run, sizeof(run));
    json_string(case_id == NULL ? "" : case_id, case_value, sizeof(case_value));
    json_string(trace_id == NULL ? "" : trace_id, trace, sizeof(trace));
    json_string(program_name(), process, sizeof(process));
    snprintf(
        line, sizeof(line),
        "{\"type\":\"exact-read.trace.started\",\"schema_version\":\"exact-read-1\",\"run_id\":%s,\"case_id\":%s,\"trace_id\":%s,\"source\":\"dyld-read-interposer\",\"authority\":\"process-returned-bytes\",\"status\":\"available\",\"capture_mode\":\"exact\",\"pid\":%d,\"process\":%s}",
        run, case_value, trace, (int)getpid(), process
    );
    emit_json(line);
    snprintf(
        line, sizeof(line),
        "{\"type\":\"exact-read.process.started\",\"run_id\":%s,\"case_id\":%s,\"trace_id\":%s,\"pid\":%d,\"process\":%s}",
        run, case_value, trace, (int)getpid(), process
    );
    emit_json(line);
}

static void emit_gap(const char *reason, const char *path) {
    char run[512], case_value[512], trace[512], reason_json[512], path_json[PATH_MAX + 64], line[PATH_MAX + 1800];
    json_string(run_id == NULL ? "" : run_id, run, sizeof(run));
    json_string(case_id == NULL ? "" : case_id, case_value, sizeof(case_value));
    json_string(trace_id == NULL ? "" : trace_id, trace, sizeof(trace));
    json_string(reason, reason_json, sizeof(reason_json));
    json_string(path == NULL ? "" : path, path_json, sizeof(path_json));
    snprintf(
        line, sizeof(line),
        "{\"type\":\"exact-read.gap\",\"run_id\":%s,\"case_id\":%s,\"trace_id\":%s,\"pid\":%d,\"process\":%s,\"reason\":%s,\"path\":%s}",
        run, case_value, trace, (int)getpid(), "\"interposer\"", reason_json, path_json
    );
    emit_json(line);
}

static struct fd_entry *find_fd(int fd) {
    for (struct fd_entry *entry = fd_entries; entry != NULL; entry = entry->next) {
        if (entry->fd == fd) return entry;
    }
    return NULL;
}

static void register_fd(int fd, const char *path, int readable) {
    if (fd < 0 || path == NULL) return;
    struct fd_entry *entry = (struct fd_entry *)calloc(1, sizeof(*entry));
    if (entry == NULL) return;
    entry->fd = fd;
    entry->path = strdup(path);
    entry->readable = readable;
    pthread_mutex_lock(&state_lock);
    entry->next = fd_entries;
    fd_entries = entry;
    pthread_mutex_unlock(&state_lock);
}

static void unregister_fd(int fd) {
    pthread_mutex_lock(&state_lock);
    struct fd_entry **cursor = &fd_entries;
    while (*cursor != NULL) {
        if ((*cursor)->fd == fd) {
            struct fd_entry *removed = *cursor;
            *cursor = removed->next;
            free(removed->path);
            free(removed);
            break;
        }
        cursor = &(*cursor)->next;
    }
    pthread_mutex_unlock(&state_lock);
}

static void copy_fd_registration(int source_fd, int destination_fd) {
    if (destination_fd < 0) return;
    pthread_mutex_lock(&state_lock);
    struct fd_entry *source = find_fd(source_fd);
    char *path = source == NULL ? NULL : strdup(source->path);
    int readable = source == NULL ? 0 : source->readable;
    pthread_mutex_unlock(&state_lock);
    if (source != NULL) {
        register_fd(destination_fd, path, readable);
    }
    free(path);
}

static char *absolute_path(const char *path) {
    if (path == NULL) return NULL;
    if (path[0] == '/') return strdup(path);
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof(cwd)) == NULL) return strdup(path);
    size_t length = strlen(cwd) + 1 + strlen(path) + 1;
    char *result = (char *)malloc(length);
    if (result == NULL) return NULL;
    snprintf(result, length, "%s/%s", cwd, path);
    return result;
}

static void emit_snapshot(const char *path, int fd) {
    if (path == NULL || real_fstat == NULL || real_pread == NULL) return;
    struct stat info;
    if (real_fstat(fd, &info) != 0 || !S_ISREG(info.st_mode) || info.st_size < 0) {
        return;
    }
    if ((uintmax_t)info.st_size > SIZE_MAX) {
        emit_gap("file-too-large-for-snapshot", path);
        return;
    }
    size_t length = (size_t)info.st_size;
    unsigned char *content = length == 0 ? NULL : (unsigned char *)malloc(length);
    if (length > 0 && content == NULL) {
        emit_gap("snapshot-allocation-failed", path);
        return;
    }
    size_t received = 0;
    while (received < length) {
        ssize_t count = real_pread(fd, content + received, length - received, (off_t)received);
        if (count <= 0) {
            free(content);
            emit_gap("snapshot-read-failed", path);
            return;
        }
        received += (size_t)count;
    }
    char hash[65];
    sha256_hex(content, length, hash);
    char *encoded = base64_encode(content, length);
    if (encoded == NULL) {
        free(content);
        emit_gap("snapshot-encoding-failed", path);
        return;
    }
    size_t encoded_capacity = ((length + 2) / 3) * 4 + 3;
    char *encoded_json = (char *)malloc(encoded_capacity);
    size_t line_capacity = encoded_capacity + PATH_MAX + 2200;
    char *line = (char *)malloc(line_capacity);
    if (encoded_json == NULL || line == NULL) {
        free(encoded_json);
        free(line);
        free(encoded);
        free(content);
        emit_gap("snapshot-record-allocation-failed", path);
        return;
    }
    char run[512], case_value[512], trace[512], path_json[PATH_MAX + 64];
    json_string(run_id == NULL ? "" : run_id, run, sizeof(run));
    json_string(case_id == NULL ? "" : case_id, case_value, sizeof(case_value));
    json_string(trace_id == NULL ? "" : trace_id, trace, sizeof(trace));
    json_string(path, path_json, sizeof(path_json));
    json_string(encoded, encoded_json, encoded_capacity);
    snprintf(
        line, line_capacity,
        "{\"type\":\"exact-read.file.snapshot\",\"run_id\":%s,\"case_id\":%s,\"trace_id\":%s,\"path\":%s,\"file_size\":%zu,\"content_base64\":%s,\"content_sha256\":\"%s\"}",
        run, case_value, trace, path_json, length, encoded_json, hash
    );
    emit_json(line);
    pthread_mutex_lock(&state_lock);
    struct snapshot_entry *snapshot = (struct snapshot_entry *)calloc(1, sizeof(*snapshot));
    if (snapshot != NULL) {
        snapshot->path = strdup(path);
        memcpy(snapshot->hash, hash, sizeof(snapshot->hash));
        snapshot->next = snapshots;
        snapshots = snapshot;
    }
    pthread_mutex_unlock(&state_lock);
    free(encoded);
    free(content);
    free(encoded_json);
    free(line);
}

static void maybe_snapshot(const char *path, int fd) {
    if (path == NULL) return;
    pthread_mutex_lock(&state_lock);
    bool known = false;
    for (struct snapshot_entry *snapshot = snapshots; snapshot != NULL; snapshot = snapshot->next) {
        if (strcmp(snapshot->path, path) == 0) {
            known = true;
            break;
        }
    }
    pthread_mutex_unlock(&state_lock);
    if (!known) emit_snapshot(path, fd);
}

static void emit_access(const char *path, const char *file_hash, off_t offset, const unsigned char *content, size_t length) {
    if (path == NULL || content == NULL || length == 0) return;
    char *encoded = base64_encode(content, length);
    if (encoded == NULL) {
        emit_gap("content-encoding-failed", path);
        return;
    }
    size_t encoded_capacity = ((length + 2) / 3) * 4 + 3;
    char *encoded_json = (char *)malloc(encoded_capacity);
    size_t line_capacity = encoded_capacity + PATH_MAX + 2400;
    char *line = (char *)malloc(line_capacity);
    if (encoded_json == NULL || line == NULL) {
        free(encoded_json);
        free(line);
        free(encoded);
        emit_gap("access-record-allocation-failed", path);
        return;
    }
    char run[512], case_value[512], trace[512], path_json[PATH_MAX + 64], process[512];
    json_string(run_id == NULL ? "" : run_id, run, sizeof(run));
    json_string(case_id == NULL ? "" : case_id, case_value, sizeof(case_value));
    json_string(trace_id == NULL ? "" : trace_id, trace, sizeof(trace));
    json_string(path, path_json, sizeof(path_json));
    json_string(encoded, encoded_json, encoded_capacity);
    json_string(program_name(), process, sizeof(process));
    char content_hash[65];
    sha256_hex(content, length, content_hash);
    pthread_mutex_lock(&state_lock);
    unsigned long current_index = event_index++;
    pthread_mutex_unlock(&state_lock);
    snprintf(
        line, line_capacity,
        "{\"type\":\"exact-read.access\",\"run_id\":%s,\"case_id\":%s,\"trace_id\":%s,\"event_index\":%lu,\"pid\":%d,\"process\":%s,\"path\":%s,\"operation\":\"read\",\"evidence_kind\":\"returned\",\"offset\":%lld,\"bytes\":%zu,\"content_base64\":%s,\"content_sha256\":\"%s\",\"file_sha256\":\"%s\"}",
        run, case_value, trace, current_index, (int)getpid(), process, path_json, (long long)offset, length, encoded_json, content_hash, file_hash == NULL ? "" : file_hash
    );
    emit_json(line);
    free(encoded);
    free(encoded_json);
    free(line);
}

static void record_read(int fd, const unsigned char *content, size_t length, off_t offset) {
    if (log_fd < 0 || content == NULL || length == 0) return;
    pthread_mutex_lock(&state_lock);
    struct fd_entry *entry = find_fd(fd);
    const char *path = entry == NULL ? NULL : entry->path;
    char *path_copy = path == NULL ? NULL : strdup(path);
    char file_hash[65] = "";
    struct snapshot_entry *snapshot = NULL;
    for (snapshot = snapshots; snapshot != NULL; snapshot = snapshot->next) {
        if (path_copy != NULL && strcmp(snapshot->path, path_copy) == 0) break;
    }
    if (snapshot != NULL) memcpy(file_hash, snapshot->hash, sizeof(file_hash));
    pthread_mutex_unlock(&state_lock);
    if (path_copy != NULL && file_hash[0] != '\0') {
        emit_access(path_copy, file_hash, offset, content, length);
    } else if (path_copy != NULL) {
        emit_gap("read-without-file-snapshot", path_copy);
    } else if (real_fstat != NULL) {
        struct stat info;
        if (real_fstat(fd, &info) == 0 && S_ISREG(info.st_mode)) {
            emit_gap("read-from-unregistered-file-descriptor", NULL);
        }
    }
    if (path_copy != NULL) {
        free(path_copy);
    }
}

static int register_opened_fd(int fd, const char *path, int flags) {
    if (fd < 0 || path == NULL) return fd;
    int readable = (flags & O_WRONLY) == 0;
    char *absolute = absolute_path(path);
    register_fd(fd, absolute == NULL ? path : absolute, readable);
    if (readable && absolute != NULL) maybe_snapshot(absolute, fd);
    free(absolute);
    return fd;
}

static char *openat_path(int dirfd, const char *path) {
    if (path == NULL || path[0] == '/') return absolute_path(path);
    if (real_fcntl != NULL) {
        char directory[PATH_MAX];
        if (real_fcntl(dirfd, F_GETPATH, directory) == 0) {
            size_t length = strlen(directory) + 1 + strlen(path) + 1;
            char *result = (char *)malloc(length);
            if (result != NULL) snprintf(result, length, "%s/%s", directory, path);
            return result;
        }
    }
    return NULL;
}

__attribute__((constructor)) static void exact_read_init(void) {
    ensure_symbols();
    const char *fd_value = getenv("EFFICIENCY_EXACT_READ_FD");
    if (fd_value != NULL) log_fd = atoi(fd_value);
    run_id = getenv("EFFICIENCY_EXACT_READ_RUN_ID");
    case_id = getenv("EFFICIENCY_EXACT_READ_CASE_ID");
    trace_id = getenv("EFFICIENCY_EXACT_READ_TRACE_ID");
    if (log_fd >= 0) emit_started();
}

int open(const char *path, int flags, ...) {
    ensure_symbols();
    mode_t mode = 0;
    if ((flags & O_CREAT) != 0) {
        va_list args;
        va_start(args, flags);
        mode = (mode_t)va_arg(args, int);
        va_end(args);
    }
    int fd = (flags & O_CREAT) != 0 ? real_open(path, flags, mode) : real_open(path, flags);
    return register_opened_fd(fd, path, flags);
}

int openat(int dirfd, const char *path, int flags, ...) {
    ensure_symbols();
    mode_t mode = 0;
    if ((flags & O_CREAT) != 0) {
        va_list args;
        va_start(args, flags);
        mode = (mode_t)va_arg(args, int);
        va_end(args);
    }
    int fd = (flags & O_CREAT) != 0 ? real_openat(dirfd, path, flags, mode) : real_openat(dirfd, path, flags);
    char *resolved = openat_path(dirfd, path);
    if (resolved == NULL) {
        emit_gap("openat-path-resolution-failed", path);
    }
    int result = register_opened_fd(fd, resolved, flags);
    free(resolved);
    return result;
}

int close(int fd) {
    ensure_symbols();
    int result = real_close(fd);
    unregister_fd(fd);
    return result;
}

int dup(int oldfd) {
    ensure_symbols();
    int result = real_dup(oldfd);
    if (result >= 0) copy_fd_registration(oldfd, result);
    return result;
}

int dup2(int oldfd, int newfd) {
    ensure_symbols();
    int result = real_dup2(oldfd, newfd);
    if (result >= 0) {
        unregister_fd(newfd);
        copy_fd_registration(oldfd, result);
    }
    return result;
}

ssize_t read(int fd, void *buffer, size_t count) {
    ensure_symbols();
    off_t offset = real_lseek(fd, 0, SEEK_CUR);
    ssize_t result = real_read(fd, buffer, count);
    if (result > 0 && offset >= 0) record_read(fd, (const unsigned char *)buffer, (size_t)result, offset);
    return result;
}

ssize_t pread(int fd, void *buffer, size_t count, off_t offset) {
    ensure_symbols();
    ssize_t result = real_pread(fd, buffer, count, offset);
    if (result > 0) record_read(fd, (const unsigned char *)buffer, (size_t)result, offset);
    return result;
}

static size_t iov_length(const struct iovec *iov, int iovcnt) {
    size_t total = 0;
    for (int i = 0; i < iovcnt; i++) {
        if (SIZE_MAX - total < iov[i].iov_len) return 0;
        total += iov[i].iov_len;
    }
    return total;
}

static unsigned char *flatten_iov(const struct iovec *iov, int iovcnt, size_t length) {
    unsigned char *buffer = length == 0 ? NULL : (unsigned char *)malloc(length);
    if (length > 0 && buffer == NULL) return NULL;
    size_t cursor = 0;
    for (int i = 0; i < iovcnt; i++) {
        memcpy(buffer + cursor, iov[i].iov_base, iov[i].iov_len);
        cursor += iov[i].iov_len;
    }
    return buffer;
}

ssize_t readv(int fd, const struct iovec *iov, int iovcnt) {
    ensure_symbols();
    off_t offset = real_lseek(fd, 0, SEEK_CUR);
    ssize_t result = real_readv(fd, iov, iovcnt);
    if (result > 0 && offset >= 0) {
        size_t total = iov_length(iov, iovcnt);
        size_t length = (size_t)result < total ? (size_t)result : total;
        unsigned char *buffer = flatten_iov(iov, iovcnt, length);
        if (buffer != NULL) record_read(fd, buffer, length, offset);
        free(buffer);
    }
    return result;
}

ssize_t preadv(int fd, const struct iovec *iov, int iovcnt, off_t offset) {
    ensure_symbols();
    ssize_t result = real_preadv(fd, iov, iovcnt, offset);
    if (result > 0) {
        size_t total = iov_length(iov, iovcnt);
        size_t length = (size_t)result < total ? (size_t)result : total;
        unsigned char *buffer = flatten_iov(iov, iovcnt, length);
        if (buffer != NULL) record_read(fd, buffer, length, offset);
        free(buffer);
    }
    return result;
}

void *mmap(void *address, size_t length, int protection, int flags, int fd, off_t offset) {
    ensure_symbols();
    void *result = real_mmap(address, length, protection, flags, fd, offset);
    if (result != MAP_FAILED && (protection & PROT_READ) != 0) {
        pthread_mutex_lock(&state_lock);
        struct fd_entry *entry = find_fd(fd);
        const char *path = entry == NULL ? NULL : entry->path;
        char *path_copy = path == NULL ? NULL : strdup(path);
        pthread_mutex_unlock(&state_lock);
        emit_gap("mmap-read-unsupported", path_copy);
        free(path_copy);
    }
    return result;
}

int munmap(void *address, size_t length) {
    ensure_symbols();
    return real_munmap(address, length);
}

ssize_t write(int fd, const void *buffer, size_t count) {
    ensure_symbols();
    pthread_mutex_lock(&state_lock);
    struct fd_entry *entry = find_fd(fd);
    const char *path = entry == NULL ? NULL : entry->path;
    char *path_copy = path == NULL ? NULL : strdup(path);
    pthread_mutex_unlock(&state_lock);
    emit_gap("file-write-unsupported", path_copy);
    free(path_copy);
    return real_write(fd, buffer, count);
}

ssize_t pwrite(int fd, const void *buffer, size_t count, off_t offset) {
    ensure_symbols();
    pthread_mutex_lock(&state_lock);
    struct fd_entry *entry = find_fd(fd);
    const char *path = entry == NULL ? NULL : entry->path;
    char *path_copy = path == NULL ? NULL : strdup(path);
    pthread_mutex_unlock(&state_lock);
    emit_gap("file-write-unsupported", path_copy);
    free(path_copy);
    return real_pwrite(fd, buffer, count, offset);
}

ssize_t writev(int fd, const struct iovec *iov, int iovcnt) {
    ensure_symbols();
    pthread_mutex_lock(&state_lock);
    struct fd_entry *entry = find_fd(fd);
    const char *path = entry == NULL ? NULL : entry->path;
    char *path_copy = path == NULL ? NULL : strdup(path);
    pthread_mutex_unlock(&state_lock);
    emit_gap("file-write-unsupported", path_copy);
    free(path_copy);
    return real_writev(fd, iov, iovcnt);
}

/* libc uses private cancellation-safe entry points for several runtimes. */
int open_nocancel(const char *path, int flags, ...) __asm("open$NOCANCEL");
int open_nocancel(const char *path, int flags, ...) {
    mode_t mode = 0;
    if ((flags & O_CREAT) != 0) {
        va_list args;
        va_start(args, flags);
        mode = (mode_t)va_arg(args, int);
        va_end(args);
        return open(path, flags, mode);
    }
    return open(path, flags);
}

int openat_nocancel(int dirfd, const char *path, int flags, ...) __asm("openat$NOCANCEL");
int openat_nocancel(int dirfd, const char *path, int flags, ...) {
    mode_t mode = 0;
    if ((flags & O_CREAT) != 0) {
        va_list args;
        va_start(args, flags);
        mode = (mode_t)va_arg(args, int);
        va_end(args);
        return openat(dirfd, path, flags, mode);
    }
    return openat(dirfd, path, flags);
}

ssize_t read_nocancel(int fd, void *buffer, size_t count) __asm("read$NOCANCEL");
ssize_t read_nocancel(int fd, void *buffer, size_t count) {
    return read(fd, buffer, count);
}

ssize_t pread_nocancel(int fd, void *buffer, size_t count, off_t offset) __asm("pread$NOCANCEL");
ssize_t pread_nocancel(int fd, void *buffer, size_t count, off_t offset) {
    return pread(fd, buffer, count, offset);
}

ssize_t readv_nocancel(int fd, const struct iovec *iov, int iovcnt) __asm("readv$NOCANCEL");
ssize_t readv_nocancel(int fd, const struct iovec *iov, int iovcnt) {
    return readv(fd, iov, iovcnt);
}

ssize_t preadv_nocancel(int fd, const struct iovec *iov, int iovcnt, off_t offset) __asm("preadv$NOCANCEL");
ssize_t preadv_nocancel(int fd, const struct iovec *iov, int iovcnt, off_t offset) {
    return preadv(fd, iov, iovcnt, offset);
}

/* Two-level namespace safe interposition for modern dyld. */
#define DYLD_INTERPOSE(_replacement, _replacee) \
    __attribute__((used)) static volatile struct { \
        const void *replacement; \
        const void *replacee; \
    } _interpose_##_replacee \
        __attribute__((section("__DATA,__interpose"))) = { \
            (const void *)(unsigned long)&_replacement, \
            (const void *)(unsigned long)&_replacee \
        };

DYLD_INTERPOSE(open, open)
DYLD_INTERPOSE(openat, openat)
DYLD_INTERPOSE(close, close)
DYLD_INTERPOSE(read, read)
DYLD_INTERPOSE(pread, pread)
DYLD_INTERPOSE(readv, readv)
DYLD_INTERPOSE(preadv, preadv)
DYLD_INTERPOSE(mmap, mmap)
DYLD_INTERPOSE(write, write)
DYLD_INTERPOSE(pwrite, pwrite)
DYLD_INTERPOSE(writev, writev)
DYLD_INTERPOSE(dup, dup)
DYLD_INTERPOSE(dup2, dup2)
