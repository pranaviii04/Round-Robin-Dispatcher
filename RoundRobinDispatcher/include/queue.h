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
