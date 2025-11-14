# Introduction

This project implements a Round Robin (RR) CPU Scheduler, following the
principles described in William Stallings' *Operating Systems* textbook.
The goal is to simulate process management, context switching, and
time-sharing using actual operating system primitives such as `fork()`,
`exec()`, `SIGTSTP`, `SIGCONT`, and `SIGINT`.

Each job is executed as a real child process under Linux/WSL. The
dispatcher controls execution through POSIX signals. The scheduler uses
a time quantum of one second, matching the example described in
Stallings Figure 9.5.

The system also includes a detailed logging mechanism and Gantt chart
timeline generation for analysis.

# Project Overview

The dispatcher performs the following tasks:

1.  Load all jobs from an input dispatch list file.

2.  Insert processes into an input queue based on arrival time.

3.  Move newly arrived processes into the Round Robin ready queue.

4.  If a process is currently executing:

    -   Decrement its remaining CPU time.

    -   If the process completes, terminate it.

    -   If its quantum expires, suspend it and re-enqueue it.

5.  If no process is running and the RR queue is non-empty, start or
    resume the next process.

6.  Log every event and record a per-second timeline.

7.  Continue scheduling until all processes have completed.

Worker programs created using `fork()` simulate CPU load through
infinite loops. The dispatcher controls each child using signals,
thereby simulating real OS behavior.

# Features

-   Round Robin scheduling with a one-second time quantum.

-   Automatic process control:

    -   Creation via `fork()`/`exec()`

    -   Suspension via `SIGTSTP`

    -   Resumption via `SIGCONT`

    -   Termination via `SIGINT`

-   Two ready queues:

    -   Input queue

    -   Round Robin ready queue

-   Detailed logging system:

    -   Start, suspend, resume, terminate events

    -   Per-second execution timeline

-   Gantt chart data export in CSV format.

-   Works on Linux and WSL2 environments.

# Folder Structure

    RoundRobinDispatcher/
    │
    ├── include/
    │   ├── common.h
    │   ├── process.h
    │   ├── queue.h
    │   ├── iohandler.h
    │   ├── logger.h
    │   ├── tester.h
    │
    ├── src/
    │   ├── dispatcher.cpp
    │   ├── process.cpp
    │   ├── iohandler.cpp
    │   ├── logger.cpp
    │   ├── queue.cpp
    │   ├── job.cpp
    │   ├── tester.cpp
    │
    ├── data/
    │   ├── dispatchlist.txt
    │   ├── log.txt
    │   ├── gantt.csv
    │
    └── Makefile

# Team Roles

-   **Aadarsh** -- Core Dispatcher Logic

-   **Praveen** -- Queue Management

-   **Pranavi** -- I/O and Logger

-   **Srihitha** -- Testing and Documentation

# Build and Run Instructions

This project requires Linux or WSL2 due to the reliance on `fork()`,
`exec()`, and POSIX signals.

To compile and run the project:

``` {.bash language="bash"}
make
make run
```

This compiles both the dispatcher and the job program, then launches the
Round Robin scheduler.

# Input Format

The dispatch list file (`dispatchlist.txt`) must contain job entries
formatted as:

    arrival_time, priority, total_cpu_time, ...

Example:

    0, 3, 3
    2, 3, 6
    4, 3, 4
    6, 3, 5
    8, 3, 2

Only the first three fields are used; additional fields are ignored.

# Output Files

After execution, the following files are generated in the `data/`
directory:

## 1. log.txt {#log.txt .unnumbered}

A chronological record of all scheduler events:

    [   0s] Job 1 - started (remaining: 3)
    [   1s] Job 1 - suspended (remaining: 2)
    [   1s] Job 2 - started (remaining: 6)
    ...

## 2. gantt.csv {#gantt.csv .unnumbered}

A per-second timeline showing which job was running:

    time,jobId
    0,1
    1,2
    2,3
    3,1
    ...

This can be used to produce a Gantt chart in Excel or a plotting script.

# Dependencies

Install the required Linux packages using:

``` {.bash language="bash"}
sudo apt update
sudo apt install g++ make build-essential
```

Windows users should use WSL2 (Ubuntu) for compatibility.

# Dispatcher Logic Summary

The Round Robin dispatcher uses:

-   `fork()` to spawn child processes.

-   `exec()` to replace the child with the job program.

-   `SIGTSTP` to pause execution.

-   `SIGCONT` to resume execution.

-   `SIGINT` to terminate execution.

Each iteration reduces the remaining CPU time and determines whether to
continue, suspend, or terminate the current job. All state changes are
logged.

# Testing

The `tester.cpp` module provides basic automated tests using:

``` {.bash language="bash"}
make run
```

Tests verify:

-   Queue transitions

-   Process start/suspend/resume events

-   Logging correctness

-   Termination behavior

-   Timeline generation accuracy

# Conclusion

This project demonstrates a functional implementation of Round Robin
scheduling using real Unix process control. It highlights key OS
concepts including process creation, context switching via signals, CPU
time management, queue design, logging, and execution timeline analysis.

The modular design allows future improvements such as priority
scheduling, multi-level feedback queues, and extended performance
metrics.

# Signatures

**Aadarsh Senapati**\
Core Dispatcher Logic

**Praveen**\
Queue Management

**Pranavi**\
I/O Handling and Logging

**Srihitha**\
Testing and Documentation
