#include <fcntl.h>
#include <sys/uio.h>
#include <unistd.h>

int main(void) {
    int fd = open("/etc/hosts", O_RDONLY);
    if (fd < 0) return 2;

    char first[8];
    if (read(fd, first, sizeof(first)) != (ssize_t)sizeof(first)) return 3;

    char positional[8];
    if (pread(fd, positional, sizeof(positional), 8) != (ssize_t)sizeof(positional)) return 4;

    int duplicate = dup(fd);
    if (duplicate < 0) return 5;
    char vector_a[4];
    char vector_b[4];
    struct iovec vectors[] = {
        {.iov_base = vector_a, .iov_len = sizeof(vector_a)},
        {.iov_base = vector_b, .iov_len = sizeof(vector_b)},
    };
    if (readv(duplicate, vectors, 2) != 8) return 6;

    char positional_vector_a[4];
    char positional_vector_b[4];
    struct iovec positional_vectors[] = {
        {.iov_base = positional_vector_a, .iov_len = sizeof(positional_vector_a)},
        {.iov_base = positional_vector_b, .iov_len = sizeof(positional_vector_b)},
    };
    if (preadv(fd, positional_vectors, 2, 24) != 8) return 7;

    close(duplicate);
    close(fd);
    return 0;
}
