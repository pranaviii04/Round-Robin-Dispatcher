#include <iostream>
#include <signal.h>
#include <unistd.h>

void sigHandler(int sig) {
    if (sig == SIGINT) {
        // Child terminates
        exit(0);
    }
}

int main() {
    signal(SIGINT, sigHandler);
    signal(SIGTSTP, SIG_IGN);
    signal(SIGCONT, SIG_IGN);

    while (true) {
        // Waste CPU time
        for (int i = 0; i < 100000000; i++);
    }
    return 0;
}
