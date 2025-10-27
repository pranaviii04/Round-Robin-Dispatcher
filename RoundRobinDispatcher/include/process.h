#ifndef PROCESS_H
#define PROCESS_H
#include "common.h"
class Process {
public:
    int pid, arrivalTime, remainingTime;
    bool started, finished;
    Process(int id, int arrival, int cpu);
    void start();
    void resume();
    void runCycle();
};
#endif
