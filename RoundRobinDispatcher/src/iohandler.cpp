#include "../include/iohandler.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <algorithm>

// trim utility
static inline std::string trim(const std::string &s) {
    size_t a = s.find_first_not_of(" \t\r\n");
    if (a == std::string::npos) return "";
    size_t b = s.find_last_not_of(" \t\r\n");
    return s.substr(a, b - a + 1);
}

ProcessList IOHandler::readJobFile(const std::string &filename) {
    ProcessList jobs;
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open job list file: " << filename << "\n";
        return jobs;
    }

    std::string line;
    int jobId = 1;
    while (std::getline(file, line)) {
        line = trim(line);
        if (line.empty() || line[0] == '#') continue;

        // split by commas
        std::stringstream ss(line);
        std::string token;
        std::vector<std::string> fields;
        while (std::getline(ss, token, ',')) {
            fields.push_back(trim(token));
        }

        if (fields.size() < 3) {
            std::cerr << "Skipping malformed line: " << line << "\n";
            continue;
        }

        try {
            int arrival = std::stoi(fields[0]);
            int priority = std::stoi(fields[1]);
            int total = std::stoi(fields[2]);

            Process *p = new Process(jobId++, arrival, total);
            p->priority = priority;
            jobs.push_back(p);
        }
        catch (...) {
            std::cerr << "Skipping corrupt line: " << line << "\n";
            continue;
        }
    }

    // sort by arrival time, then jobId
    std::sort(jobs.begin(), jobs.end(),
        [](const Process* a, const Process* b) {
            if (a->arrivalTime == b->arrivalTime)
                return a->jobId < b->jobId;
            return a->arrivalTime < b->arrivalTime;
        }
    );

    return jobs;
}

void IOHandler::loadArrived(ProcessQueue &input, ProcessQueue &rr, int timer) {
    while (!input.empty()) {
        Process* p = input.front();
        if (p->arrivalTime <= timer)
            rr.enqueue(input.dequeue());
        else
            break;
    }
}

void IOHandler::freeProcessList(ProcessList &plist) {
    for (auto p : plist) delete p;
    plist.clear();
}
