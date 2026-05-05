#!/usr/bin/env python3
import sys
import time

try:
    import networkx as nx
except ImportError as exc:
    print("Error: networkx is not installed. Install with: pip install networkx")
    raise SystemExit(1) from exc


def read_graph(path, weighted):
    with open(path, "r", encoding="utf-8") as handle:
        header = handle.readline().strip().split()
        if len(header) < 2:
            raise ValueError("Invalid header: expected 'V E' on first line")
        v_count = int(header[0])
        e_count = int(header[1])

        graph = nx.Graph()
        graph.add_nodes_from(range(v_count))
        for _ in range(e_count):
            parts = handle.readline().strip().split()
            if not parts:
                continue
            if weighted:
                if len(parts) < 3:
                    raise ValueError("Weighted edge missing weight")
                u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                graph.add_edge(u, v, weight=w)
            else:
                if len(parts) < 2:
                    raise ValueError("Unweighted edge missing endpoint")
                u, v = int(parts[0]), int(parts[1])
                graph.add_edge(u, v)

    return graph


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 compare.py <filename> <is_weighted (0 or 1)>")
        return 1

    filename = sys.argv[1]
    weighted = bool(int(sys.argv[2]))

    graph = read_graph(filename, weighted)

    start = time.perf_counter()
    if weighted:
        centrality = nx.closeness_centrality(graph, distance="weight")
    else:
        centrality = nx.closeness_centrality(graph)
    elapsed = time.perf_counter() - start

    node_id = 60
    node_score = centrality.get(node_id, 0.0)
    with open("networkx_time.txt", "w", encoding="utf-8") as handle:
        handle.write(f"Computation took: {elapsed:.6f} seconds.\n")
        handle.write(f"Node ({node_id}) score: {node_score}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())