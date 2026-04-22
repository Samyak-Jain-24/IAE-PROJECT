CXX = g++
CXXFLAGS = -std=c++20 -O3 -fopenmp

all: centrality

centrality: main.o graph.o
	$(CXX) $(CXXFLAGS) main.o graph.o -o centrality

main.o: main.cpp graph.hpp
	$(CXX) $(CXXFLAGS) -c main.cpp

graph.o: graph.cpp graph.hpp
	$(CXX) $(CXXFLAGS) -c graph.cpp

clean:
	rm -f *.o centrality