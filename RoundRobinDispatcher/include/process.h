#ifndef PROCESS_H
#define PROCESS_H

#include "common.h"

struct Process {
    int jobId;
    int arrivalTime;
    int priority;
    int totalTime;
    int remainingTime;
    int osPid;       // assigned after fork() in dispatcher
    bool started;
    bool finished;

    Process()
        : jobId(-1), arrivalTime(0), priority(0), totalTime(0),
          remainingTime(0), osPid(-1), started(false), finished(false) {}

    Process(int id, int arrival, int total)
        : jobId(id), arrivalTime(arrival), priority(0), totalTime(total),
          remainingTime(total), osPid(-1), started(false), finished(false) {}
};

using ProcessList = std::vector<Process*>;

void startProcess(Process* p);     // fork + exec
void suspendProcess(Process* p);   // SIGTSTP
void resumeProcess(Process* p);    // SIGCONT
void terminateProcess(Process* p); // SIGINT

#endif // PROCESS_H
