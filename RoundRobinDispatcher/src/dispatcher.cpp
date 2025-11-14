#include "../include/iohandler.h"
#include "../include/logger.h"
#include "../include/process.h"
#include "../include/queue.h"

#include <unistd.h>     // sleep, fork
#include <signal.h>     // SIGCONT, SIGTSTP, SIGINT
#include <sys/types.h>  // pid_t
#include <iostream>

int main() {
    ProcessList jobs = IOHandler::readJobFile("data/dispatchlist.txt");

    ProcessQueue inputQ;
    for (auto p : jobs) inputQ.enqueue(p);

    ProcessQueue rrQ;

    Logger logger("data/log.txt", "data/gantt.csv");

    int timer = 0;
    Process* current = nullptr;

    while (!inputQ.empty() || !rrQ.empty() || current != nullptr) {

        IOHandler::loadArrived(inputQ, rrQ, timer);

        if (current != nullptr) {

            current->remainingTime--;

            logger.setTimelineEntry(timer, current->jobId);

            if (current->remainingTime <= 0) {
                logger.log(timer, current->jobId, "terminated", 0);
                terminateProcess(current);
                current = nullptr;
            }
            else if (!rrQ.empty()) {
                logger.log(timer, current->jobId, "suspended", current->remainingTime);
                suspendProcess(current);
                rrQ.enqueue(current);
                current = nullptr;
            }
        }
        else {
            logger.setTimelineEntry(timer, -1);
        }

        if (current == nullptr && !rrQ.empty()) {
            current = rrQ.dequeue();

            if (!current->started) {
                logger.log(timer, current->jobId, "started", current->remainingTime);
                startProcess(current);
                usleep(200000);
            }
            else {
                logger.log(timer, current->jobId, "resumed", current->remainingTime);
                resumeProcess(current);
            }
        }

        sleep(1);
        timer++;
    }

    logger.exportLogs();
    IOHandler::freeProcessList(jobs);

    return 0;
}
