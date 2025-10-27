// iohandler.cpp - Pranavi
#include "../include/iohandler.h"
vector<Process> IOHandler::readJobFile(string filename) {
    vector<Process> jobs; ifstream file(filename);
    int arrival, pri, cpu, rest, id = 1;
    while (file >> arrival) {
        file.ignore(1, ','); file >> pri; file.ignore(1, ',');
        file >> cpu; file.ignore(256, '\n');
        jobs.emplace_back(id++, arrival, cpu);
    }
    return jobs;
}
void IOHandler::loadArrived(ProcessQueue &input, ProcessQueue &rr, int timer) {
    while (!input.empty() && input.front()->arrivalTime <= timer)
        rr.enqueue(input.dequeue());
}
