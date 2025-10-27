// dispatcher.cpp - Aadarsh
#include "../include/common.h"
#include "../include/process.h"
#include "../include/queue.h"
#include "../include/iohandler.h"
#include "../include/logger.h"
#include <thread>
#include <chrono>
#include <iostream>

using namespace std;

int main() {
    cout << "=== Round Robin Dispatcher Simulation Started ===" << endl;
    int dispatcherTimer = 0, quantum = 1;
    ProcessQueue inputQueue, rrQueue;
    vector<Process> processes = IOHandler::readJobFile("data/dispatchlist.txt");
    for (auto &p : processes) inputQueue.enqueue(&p);
    Process* current = nullptr;

    while (!inputQueue.empty() || !rrQueue.empty() || current != nullptr) {
        IOHandler::loadArrived(inputQueue, rrQueue, dispatcherTimer);
        if (current) {
            current->runCycle();
            if (current->remainingTime <= 0) {
                Logger::log("Process " + to_string(current->pid) + " completed.");
                current = nullptr;
            } else {
                Logger::log("Process " + to_string(current->pid) + " suspended.");
                rrQueue.enqueue(current);
                current = nullptr;
            }
        if (!current && !rrQueue.empty()) {
            current = rrQueue.dequeue();
            if (!current->started) current->start();
            else current->resume();
        }
        std::this_thread::sleep_for(std::chrono::seconds(1));
        dispatcherTimer++;
    }
    }

    cout << "=== Dispatcher Finished ===" << endl;
    return 0;
}
