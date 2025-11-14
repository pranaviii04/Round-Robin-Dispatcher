CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude

SRC = src/dispatcher.cpp src/process.cpp src/iohandler.cpp src/logger.cpp src/queue.cpp
JOB = src/job.cpp

all: build/job build/dispatcher

build/dispatcher: $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o build/dispatcher

build/job: $(JOB)
	$(CXX) $(CXXFLAGS) $(JOB) -o build/job

clean:
	rm -rf build/dispatcher build/job
