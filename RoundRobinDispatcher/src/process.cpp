#include "../include/process.h"
#include <unistd.h>
#include <signal.h>
#include <iostream>

void startProcess(Process* p) {
    pid_t pid = fork();

    if (pid < 0) {
        std::cerr << "Error: fork() failed for job " << p->jobId << "\n";
        return;
    }

    if (pid == 0) {
        // child: replace with CPU job file
        execl("./build/job", "job", NULL);
        std::cerr << "Error: exec() failed\n";
        exit(1);
    }

    // parent: store OS PID
    p->osPid = pid;
    p->started = true;
}

void suspendProcess(Process* p) {
    if (p->osPid > 0)
        kill(p->osPid, SIGTSTP);
}

void resumeProcess(Process* p) {
    if (p->osPid > 0)
        kill(p->osPid, SIGCONT);
}

void terminateProcess(Process* p) {
    if (p->osPid > 0)
        kill(p->osPid, SIGINT);
    p->finished = true;
}
