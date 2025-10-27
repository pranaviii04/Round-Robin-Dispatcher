// process.cpp - Aadarsh
#include "../include/process.h"
#include "../include/logger.h"

Process::Process(int id, int arrival, int cpu) {
    pid = id; 
    arrivalTime = arrival; 
    remainingTime = cpu;
    started = false; 
    finished = false;
}
void Process::start() { 
    started = true; 
    Logger::log("Process " + to_string(pid) + " started."); 
}
void Process::resume() { 
    Logger::log("Process " + to_string(pid) + " resumed.");
}
void Process::runCycle() { 
    if (remainingTime > 0) {
        remainingTime--; 
        Logger::log("Process " + to_string(pid) + " ran for 1 time unit. Remaining time: " + to_string(remainingTime) + ".");
        if (remainingTime == 0 && !finished) {
        finished = true;
        Logger::log("Process " + to_string(pid) + " finished execution.");
    }
    }

}
