#ifndef IOHANDLER_H
#define IOHANDLER_H

#include "common.h"
#include "process.h"
#include "queue.h"
#include <string>
#include <vector>

class IOHandler {
public:
    static ProcessList readJobFile(const std::string &filename);
    static void loadArrived(ProcessQueue &input, ProcessQueue &rr, int timer);
    static void freeProcessList(ProcessList &plist);
};

#endif // IOHANDLER_H
