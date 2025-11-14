#include "../include/logger.h"
#include <sstream>
#include <iostream>
#include <iomanip>

Logger::Logger(const std::string &logPath, const std::string &ganttPath)
    : logPath_(logPath), ganttPath_(ganttPath)
{
    logfile_.open(logPath_, std::ios::out);
    if (!logfile_.is_open())
        std::cerr << "Logger: Cannot open " << logPath_ << "\n";
}

Logger::~Logger() {
    exportLogs();
    if (logfile_.is_open()) logfile_.close();
}

void Logger::log(int timeSec, int jobId, const std::string &action, int remaining) {
    std::lock_guard<std::mutex> lock(mtx_);
    std::ostringstream ss;

    ss << "[" << std::setw(4) << timeSec << "s] ";
    ss << "Job " << jobId << " - " << action;
    if (remaining >= 0) ss << " (remaining: " << remaining << ")";

    std::string line = ss.str();
    textlog_.push_back(line);

    std::cout << line << std::endl;
    if (logfile_.is_open()) logfile_ << line << std::endl;
}

void Logger::setTimelineEntry(int timeSec, int jobId) {
    std::lock_guard<std::mutex> lock(mtx_);
    timeline_[timeSec] = jobId;
}

void Logger::exportLogs() {
    std::lock_guard<std::mutex> lock(mtx_);

    std::ofstream gout(ganttPath_, std::ios::out);
    if (!gout.is_open()) {
        std::cerr << "Logger: Cannot open " << ganttPath_ << "\n";
        return;
    }

    gout << "time,jobId\n";
    for (auto &kv : timeline_)
        gout << kv.first << "," << kv.second << "\n";

    gout.close();
}
