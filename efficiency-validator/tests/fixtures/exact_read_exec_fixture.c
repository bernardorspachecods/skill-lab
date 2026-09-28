#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    pid_t child = fork();
    if (child < 0) return 3;
    if (child == 0) {
        execl(argv[1], argv[1], (char *)NULL);
        _exit(4);
    }
    int status = 0;
    if (waitpid(child, &status, 0) < 0) return 5;
    return WIFEXITED(status) ? WEXITSTATUS(status) : 6;
}
