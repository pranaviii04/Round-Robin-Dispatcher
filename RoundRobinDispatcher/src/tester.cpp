// tester.cpp - Srihitha
#include "../include/tester.h"
#include <iostream>
void Tester::runTests() {
    std::cout << "Running basic test cases..." << endl;
    system("make run");
    cout << "Check data/log.txt for output validation." << endl;
}
