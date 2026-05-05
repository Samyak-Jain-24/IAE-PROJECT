#!/usr/bin/env python3
import sys
import time

try:
    import networkx as nx
except ImportError as exc:
    print("Error: networkx is not installed. Install with: pip install networkx")
    raise SystemExit(1) from exc


def read_weighted_graph(path, directed):
    with open(path, "r", encoding="utf-8") as handle:
        header = handle.readline().strip().split()
        if len(header) < 2:
            raise ValueError("Invalid header: expected 'V E' on first line")
        v_count = int(header[0])
        e_count = int(header[1])

        graph = nx.DiGraph() if directed else nx.Graph()
        graph.add_nodes_from(range(v_count))
        for _ in range(e_count):
            parts = handle.readline().strip().split()
            if not parts:
                continue
            if len(parts) < 3:
                raise ValueError("Weighted edge missing weight")
            u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
            graph.add_edge(u, v, weight=w)

    return graph


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 compare_weighted.py <filename> <is_directed (0 or 1)>")
        return 1

    filename = sys.argv[1]
    directed = bool(int(sys.argv[2]))
    graph = read_weighted_graph(filename, directed)

    start = time.perf_counter()
    centrality = nx.closeness_centrality(graph, distance="weight")
    elapsed = time.perf_counter() - start

    node_id = 60
    node_score = centrality.get(node_id, 0.0)
    with open("networkx_weighted_time.txt", "w", encoding="utf-8") as handle:
        handle.write(f"Computation took: {elapsed:.6f} seconds.\n")
        handle.write(f"Node ({node_id}) score: {node_score}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
