#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int main(void) {
    int fd = open("/etc/hosts", O_RDONLY);
    if (fd < 0) return 2;
    char buffer[32];
    ssize_t count = read(fd, buffer, sizeof(buffer));
    close(fd);
    if (count < 0) return 3;
    return 0;
}
