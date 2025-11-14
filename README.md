# Round Robin Dispatcher – Operating Systems Project

A complete Round Robin CPU Scheduling simulator implemented using real Linux process control mechanisms (`fork()`, `exec()`, `SIGTSTP`, `SIGCONT`, `SIGINT`).  
This project references to the Round Robin scheduler from **William Stallings' Operating Systems** textbook using actual process management.

Each job executes as a live child process under Linux/WSL2, and the dispatcher controls it using POSIX signals—simulating true context switching, CPU bursts, and quantum expiration.

---

## Features

- Round Robin scheduling (Quantum = **1 second**)
- **Process creation:** `fork()` + `exec()`
- **Context switching:**  
  - Suspend → `SIGTSTP`  
  - Resume → `SIGCONT`  
  - Terminate → `SIGINT`
- Two queues:
  - Input queue (arrival-based)
  - Round Robin ready queue
- Detailed event logging (`log.txt`)
- Automatic per-second timeline generation (`gantt.csv`)
- Optional Gantt chart visualization (`Python`)
- Performance metrics (turnaround, waiting, response times, CPU utilization)

---

## 📂 Folder Structure
```
RoundRobinDispatcher/
│
├── include/
│ ├── common.h
│ ├── process.h
│ ├── queue.h
│ ├── iohandler.h
│ ├── logger.h
│ ├── tester.h
│
├── src/
│ ├── dispatcher.cpp
│ ├── process.cpp
│ ├── iohandler.cpp
│ ├── logger.cpp
│ ├── queue.cpp
│ ├── job.cpp
│ ├── tester.cpp
│
├── data/
│ ├── dispatchlist.txt
│ ├── log.txt
│ ├── gantt.csv
│ ├── gantt.png
│
├── scripts/
│ ├── parse_log_to_gantt.py
│ ├── gantt.py
│ ├── analyze_log.py
│ ├── generate_jobs.py
│
└── Makefile

```
---

## Input Format (`dispatchlist.txt`)

Each job entry:

arrival_time, priority, total_cpu_time, ...

```
Example:

0, 3, 3
2, 3, 6
4, 3, 4
6, 3, 5
8, 3, 2
```

Only the first **three** fields are used; remaining fields are ignored.

---

## Output Files

### **1. log.txt**  
Chronological event log:
```
[ 0s] Job 1 - started (remaining: 3)
[ 1s] Job 1 - suspended (remaining: 2)
[ 1s] Job 2 - started (remaining: 6)
```

### **2. gantt.csv**  
Per-second timeline:
```
time,jobId
0,1
1,2
2,3
3,1
...
```
### **3. gantt.png**  
Graphical Gantt chart generated using Python.

---

## 🛠 Build Instructions (Linux / WSL2)

This project **requires Linux** (or WSL2) because of POSIX signals.

### Install dependencies:
```bash
sudo apt update
sudo apt install -y g++ make build-essential python3 python3-pandas python3-matplotlib
```
### Build the project:
```bash
make clean
make
```
### Run the dispatcher:
```bash
./build/dispatcher
```
This generates:
1. data/log.txt
2. possibly data/gantt.csv

## 📊 Generate Gantt Chart & Statistics

### Convert log → gantt.csv:
```bash
python3 scripts/parse_log_to_gantt.py data/log.txt data/dispatchlist.txt
```
### Visualize Gantt chart:
```bash
python3 scripts/gantt.py data/gantt.csv
```
Produces:
✔ data/gantt.png

### Analyze performance metrics:
```bash
python3 scripts/analyze_log.py data/gantt.csv data/dispatchlist.txt
```
Produces:
✔ data/results.txt

## 🧪 Running Tests
Built-in tests check:
- Queue operations
- RR behavior
- Preemption logic
- Logging & timeline generation
- Termination handling

Run tests with:
```bash
make run
```
## How the Scheduler Works
1. **Job Arrival**  
&nbsp;&nbsp;&nbsp;&nbsp;Jobs move from Input Queue → RR Queue based on arrival time.

2. **Every 1 Second**  
&nbsp;&nbsp;&nbsp;&nbsp;• Decrement remaining CPU time  
&nbsp;&nbsp;&nbsp;&nbsp;• If quantum expires → `SIGTSTP` (suspend)  
&nbsp;&nbsp;&nbsp;&nbsp;• If CPU time reaches 0 → `SIGINT` (terminate)

3. **No Running Process**  
&nbsp;&nbsp;&nbsp;&nbsp;• Dequeue next job from RR Queue  
&nbsp;&nbsp;&nbsp;&nbsp;• First run → `fork()` + `exec()`  
&nbsp;&nbsp;&nbsp;&nbsp;• Resume → `SIGCONT`

4. **Log the Event**

5. **Record the Timeline Tick**


### Team Members
- Aadarsh (Core Dispatcher Logic)
- Praveen (Queue Management)
- Pranavi (I/O Handling & Logging)
- Srihitha (Testing & Documentation)

## Beginner-Friendly Quick Start
1. Install dependencies
   ```
   ./setup_project.sh
    sudo apt install g++ make python3 python3-pandas python3-matplotlib
   ```
2. Build project
   ```
   make
   ```
3. Run scheduler
   ```
   ./build/dispatcher
   ```
4. Parse log into timeline
   ```
   python3 scripts/parse_log_to_gantt.py data/log.txt data/dispatchlist.txt
   ```
5. Generate Gantt chart
   ```
   python3 scripts/gantt.py data/gantt.csv
   ```
6. Analyze metrics
   ```
   python3 scripts/analyze_log.py data/gantt.csv data/dispatchlist.txt
   ```
12. View results in /data:
   - log.txt
   - gantt.csv
   - gantt.png
   - results.txt
   - results_from_log.txt

## Signatures
Aadarsh  Praveen  Pranavi  Srihitha
