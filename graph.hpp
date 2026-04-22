#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <vector>
#include <iostream>

struct Edge {
    int to;
    int weight;
};

class Graph {
public:
    int V;
    bool isWeighted;
    std::vector<std::vector<Edge>> adj;

    Graph(int vertices, bool weighted);
    void addEdge(int u, int v, int w = 1);
    
    // Calculates the sum of shortest paths from a start node
    double getShortestPathSum(int startNode);
};

#endif