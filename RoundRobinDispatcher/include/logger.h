#ifndef LOGGER_H
#define LOGGER_H
#include "common.h"
class Logger {
public:
    static ofstream logfile;
    static void log(string msg);
};
#endif
