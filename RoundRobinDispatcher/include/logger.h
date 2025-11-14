#ifndef LOGGER_H
#define LOGGER_H

#include "common.h"
#include <string>
#include <fstream>
#include <mutex>
#include <vector>
#include <map>

class Logger {
public:
    Logger(const std::string &logPath = "data/log.txt",
           const std::string &ganttPath = "data/gantt.csv");
    ~Logger();

    void log(int timeSec, int jobId, const std::string &action, int remaining=-1);
    void setTimelineEntry(int timeSec, int jobId);
    void exportLogs();

private:
    std::string logPath_;
    std::string ganttPath_;
    std::ofstream logfile_;
    std::mutex mtx_;
    std::vector<std::string> textlog_;
    std::map<int,int> timeline_;
};

#endif // LOGGER_H
