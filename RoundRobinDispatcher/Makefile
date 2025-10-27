CXX = g++
CXXFLAGS = -std=c++17 -Wall -Iinclude
SRC = $(wildcard src/*.cpp)
OBJ = $(SRC:src/%.cpp=build/%.o)
EXEC = build/dispatcher.out

all: $(EXEC)
build/%.o: src/%.cpp | build
	$(CXX) $(CXXFLAGS) -c $< -o $@
build:
	mkdir -p build
$(EXEC): $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o $(EXEC)
run: $(EXEC)
	./$(EXEC)
clean:
	rm -rf build/*.o $(EXEC)
