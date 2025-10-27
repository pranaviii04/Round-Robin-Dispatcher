#!/bin/bash
# Round Robin Dispatcher Project Setup Script
# Author: Project Team

echo "Setting up Round Robin Dispatcher project structure..."

mkdir -p RoundRobinDispatcher/{src,include,data,docs/scripts,build,docs/ReadmeScreenshots}
cd RoundRobinDispatcher || exit

# === Source files ===
cat > src/dispatcher.cpp << 'EOF'
// dispatcher.cpp - Aadarsh
#include "../include/common.h"
#include "../include/process.h"
#include "../include/queue.h"
#include "../include/iohandler.h"
#include "../include/logger.h"

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
        }
        if (!current && !rrQueue.empty()) {
            current = rrQueue.dequeue();
            if (!current->started) current->start();
            else current->resume();
        }
        this_thread::sleep_for(chrono::seconds(1));
        dispatcherTimer++;
    }

    cout << "=== Dispatcher Finished ===" << endl;
    return 0;
}
EOF

cat > src/process.cpp << 'EOF'
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
EOF

cat > src/queue.cpp << 'EOF'
// queue.cpp - Praveen
#include "../include/queue.h"
void ProcessQueue::enqueue(Process* p) { q.push(p); }
Process* ProcessQueue::dequeue() { if (q.empty()) return nullptr; Process* p = q.front(); q.pop(); return p; }
bool ProcessQueue::empty() { return q.empty(); }
EOF

cat > src/iohandler.cpp << 'EOF'
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
EOF

cat > src/logger.cpp << 'EOF'
// logger.cpp - Pranavi
#include "../include/logger.h"
ofstream Logger::logfile("data/log.txt", ios::out);
void Logger::log(string msg) {
    string timestamp = "[" + to_string(time(nullptr)) + "] ";
    cout << timestamp << msg << endl;
    logfile << timestamp << msg << endl;
}
EOF

cat > src/tester.cpp << 'EOF'
// tester.cpp - Srihitha
#include "../include/tester.h"
void Tester::runTests() {
    cout << "Running basic test cases..." << endl;
    system("make run");
    cout << "Check data/log.txt for output validation." << endl;
}
EOF

cat > src/job.cpp << 'EOF'
// job.cpp
#include <iostream>
#include <unistd.h>
int main() {
    for (int i = 0; i < 5; i++) {
        std::cout << "Child job running: cycle " << i << std::endl;
        sleep(1);
    }
    return 0;
}
EOF

# === Headers ===
cat > include/common.h << 'EOF'
#ifndef COMMON_H
#define COMMON_H
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <queue>
#include <thread>
#include <chrono>
using namespace std;
#endif
EOF

cat > include/process.h << 'EOF'
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
EOF

cat > include/queue.h << 'EOF'
#ifndef QUEUE_H
#define QUEUE_H
#include "common.h"
#include "process.h"
class ProcessQueue {
    queue<Process*> q;
public:
    void enqueue(Process* p);
    Process* dequeue();
    bool empty();
    Process* front() { return q.front(); }
};
#endif
EOF

cat > include/iohandler.h << 'EOF'
#ifndef IOHANDLER_H
#define IOHANDLER_H
#include "common.h"
#include "queue.h"
#include "process.h"
class IOHandler {
public:
    static vector<Process> readJobFile(string filename);
    static void loadArrived(ProcessQueue &input, ProcessQueue &rr, int timer);
};
#endif
EOF

cat > include/logger.h << 'EOF'
#ifndef LOGGER_H
#define LOGGER_H
#include "common.h"
class Logger {
public:
    static ofstream logfile;
    static void log(string msg);
};
#endif
EOF

cat > include/tester.h << 'EOF'
#ifndef TESTER_H
#define TESTER_H
#include "common.h"
class Tester {
public:
    static void runTests();
};
#endif
EOF

# === Data and Makefile ===
cat > data/dispatchlist.txt << 'EOF'
0, 3, 3, 64, 0, 0, 0, 0
2, 3, 6, 64, 0, 0, 0, 0
4, 3, 4, 64, 0, 0, 0, 0
6, 3, 5, 64, 0, 0, 0, 0
8, 3, 2, 64, 0, 0, 0, 0
EOF

cat > Makefile << 'EOF'
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude
SRC = $(wildcard src/*.cpp)
OBJ = $(SRC:src/%.cpp=build/%.o)
EXEC = build/dispatcher.out

all: $(EXEC)
build/%.o: src/%.cpp | build
	$(CXX) $(CXXFLAGS) -c $< -o $@
build:
	mkdir -p build
$(EXEC): $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o $(EXEC)
run: $(EXEC)
	./$(EXEC)
clean:
	rm -rf build/*.o $(EXEC)
EOF

cat > README.md << 'EOF'
# 🧠 Round Robin Dispatcher (C++ Project)
A simulation of CPU Round Robin scheduling with process management, logging, and test validation.

### 👥 Team Roles
- **Aadarsh** – Core Dispatcher Logic  
- **Praveen** – Queue Management  
- **Pranavi** – I/O & Logger  
- **Srihitha** – Testing & Documentation  

### ⚙️ Build and Run
```bash
make
make run
EOF

echo "✅ Round Robin Dispatcher project structure created successfully!"
EOF
