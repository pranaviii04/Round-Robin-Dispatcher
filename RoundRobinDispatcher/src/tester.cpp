// tester.cpp - Srihitha
#include "../include/tester.h"
#include <iostream>
void Tester::runTests() {
    std::cout << "Running basic test cases..." << std::endl;
    system("make run");
    std::cout << "Check data/log.txt for output validation." << std::endl;
}
