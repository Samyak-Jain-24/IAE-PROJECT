#include <iostream>
#include <fstream>
#include <vector>
#include <omp.h>
#include <chrono>
#include "graph.hpp"
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: ./centrality <filename> <is_weighted (0 or 1)>" << std::endl;
        return 1;
    }

    std::string filename = argv[1];
    bool weighted = std::stoi(argv[2]);
    
    std::ifstream infile(filename);
    int V, E;
    infile >> V >> E;
    
    Graph g(V, weighted);
    for (int i = 0; i < E; i++) {
        int u, v, w = 1;
        if (weighted) infile >> u >> v >> w;
        else infile >> u >> v;
        g.addEdge(u, v, w);
    }

    std::vector<double> closeness(V);
    auto start = std::chrono::high_resolution_clock::now();

    // PARALLEL BLOCK
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < V; i++) {
        double pathSum = g.getShortestPathSum(i);
        if (pathSum > 0) {
            closeness[i] = (double)(V - 1) / pathSum;
        } else {
            closeness[i] = 0;
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    std::cout << "Computation took: " << elapsed.count() << " seconds." << std::endl;
    std::cout << "Top node (0) score: " << closeness[60] << std::endl;

    return 0;
}