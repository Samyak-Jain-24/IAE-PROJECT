#include "graph.hpp"
#include <queue>
#include <limits>

const int INF = std::numeric_limits<int>::max();

Graph::Graph(int vertices, bool weighted) : V(vertices), isWeighted(weighted) {
    adj.resize(V);
}

void Graph::addEdge(int u, int v, int w) {
    adj[u].push_back({v, w});
}

double Graph::getShortestPathSum(int startNode, int& reachableNodes) {
    std::vector<int> dist(V, INF);
    dist[startNode] = 0;
    long long totalDist = 0;
    reachableNodes = 0;

    if (!isWeighted) {
        // Unweighted: Use BFS
        std::queue<int> q;
        q.push(startNode);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto& edge : adj[u]) {
                if (dist[edge.to] == INF) {
                    dist[edge.to] = dist[u] + 1;
                    totalDist += dist[edge.to];
                    reachableNodes++;
                    q.push(edge.to);
                }
            }
        }
    } else {
        // Weighted: Use Dijkstra
        std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<>> pq;
        pq.push({0, startNode});
        while (!pq.empty()) {
            int d = pq.top().first;
            int u = pq.top().second;
            pq.pop();
            if (d > dist[u]) continue;
            for (auto& edge : adj[u]) {
                if (dist[u] + edge.weight < dist[edge.to]) {
                    dist[edge.to] = dist[u] + edge.weight;
                    pq.push({dist[edge.to], edge.to});
                }
            }
        }
        for (int i = 0; i < V; i++) {
            if (dist[i] != INF && i != startNode) {
                totalDist += dist[i];
                reachableNodes++;
            }
        }
    }
    return (reachableNodes == 0) ? 0 : (double)totalDist;
}