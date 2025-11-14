#ifndef QUEUE_H
#define QUEUE_H

#include "process.h"
#include <queue>

class ProcessQueue {
public:
    void enqueue(Process* p) { q.push(p); }

    Process* dequeue() {
        if (q.empty()) return nullptr;
        Process* p = q.front();
        q.pop();
        return p;
    }

    Process* front() const {
        return q.empty() ? nullptr : q.front();
    }

    bool empty() const { return q.empty(); }
    size_t size() const { return q.size(); }

private:
    std::queue<Process*> q;
};

#endif // QUEUE_H
