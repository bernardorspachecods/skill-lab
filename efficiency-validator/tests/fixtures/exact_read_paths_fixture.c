#include <fcntl.h>
#include <unistd.h>

int main(int argc, char **argv) {
    for (int index = 1; index < argc; index++) {
        int fd = open(argv[index], O_RDONLY);
        if (fd < 0) return 2;
        char byte;
        if (read(fd, &byte, 1) != 1) return 3;
        close(fd);
    }
    return 0;
}
