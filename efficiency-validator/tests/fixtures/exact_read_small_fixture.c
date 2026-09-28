#include <fcntl.h>
#include <unistd.h>

int main(void) {
    int fd = open("/etc/hosts", O_RDONLY);
    if (fd < 0) return 2;
    char buffer[8];
    ssize_t count = read(fd, buffer, sizeof(buffer));
    close(fd);
    return count == (ssize_t)sizeof(buffer) ? 0 : 3;
}
