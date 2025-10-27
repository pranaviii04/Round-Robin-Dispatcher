// queue.cpp - Praveen
#include "../include/queue.h"
void ProcessQueue::enqueue(Process* p) { q.push(p); }
Process* ProcessQueue::dequeue() { if (q.empty()) return nullptr; Process* p = q.front(); q.pop(); return p; }
bool ProcessQueue::empty() { return q.empty(); }
