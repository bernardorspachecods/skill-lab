#include <fcntl.h>
#include <unistd.h>

int main(void) {
    int fd = open("/etc/hosts", O_RDONLY);
    if (fd < 0) return 2;
    char buffer[32];
    if (read(fd, buffer, sizeof(buffer)) < 0) return 3;
    sleep(2);
    close(fd);
    return 0;
}
