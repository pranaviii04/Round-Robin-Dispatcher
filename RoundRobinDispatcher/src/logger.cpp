// logger.cpp - Pranavi
#include "../include/logger.h"
ofstream Logger::logfile("data/log.txt", ios::out);
void Logger::log(string msg) {
    string timestamp = "[" + to_string(time(nullptr)) + "] ";
    cout << timestamp << msg << endl;
    logfile << timestamp << msg << endl;
}
