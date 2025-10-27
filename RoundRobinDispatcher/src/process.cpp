// process.cpp - Aadarsh
#include "../include/process.h"
#include "../include/logger.h"

Process::Process(int id, int arrival, int cpu) {
    pid = id; arrivalTime = arrival; remainingTime = cpu;
    started = false; finished = false;
}
void Process::start() { started = true; Logger::log("Process " + to_string(pid) + " started."); }
void Process::resume() { Logger::log("Process " + to_string(pid) + " resumed."); }
void Process::runCycle() { if (remainingTime > 0) remainingTime--; }
