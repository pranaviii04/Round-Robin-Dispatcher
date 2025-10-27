// job.cpp
#include <iostream>
#include <unistd.h>
int main() {
    for (int i = 0; i < 5; i++) {
        std::cout << "Child job running: cycle " << i << std::endl;
        sleep(1);
    }
    return 0;
}
