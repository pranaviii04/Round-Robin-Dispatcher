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
