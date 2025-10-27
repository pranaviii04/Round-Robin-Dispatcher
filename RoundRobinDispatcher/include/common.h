#ifndef COMMON_H
#define COMMON_H
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <queue>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <ctime>
using namespace std;

// prefer qualified usage like std::this_thread::sleep_for(...)
// or enable the following if your standard library supports importing the nested namespace:
// using namespace std::this_thread;
using std::chrono::seconds;

#endif
