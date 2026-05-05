#!/usr/bin/env python3
import re
from pathlib import Path

import matplotlib.pyplot as plt


RESULT_FILES = {
    "unweighted": Path("centrality_results.txt"),
    "weighted": Path("centrality_weighted_results.txt"),
}

ALGO_COMPARISON_FILE = Path("centrality_unweighted_dijkstra_wikivote_results.txt")

NETWORKX_FILES = {
    "unweighted": Path("networkx_time.txt"),
    "weighted": Path("networkx_weighted_time.txt"),
}

OUTPUTS = {
    "unweighted": {
        "time": Path("plots/unweighted_time_vs_threads.png"),
        "speedup": Path("plots/unweighted_speedup.png"),
        "comparison": Path("plots/unweighted_cpp_vs_networkx.png"),
    },
    "weighted": {
        "time": Path("plots/weighted_time_vs_threads.png"),
        "speedup": Path("plots/weighted_speedup.png"),
        "comparison": Path("plots/weighted_cpp_vs_networkx.png"),
    },
    "algorithm": {
        "comparison": Path("plots/unweighted_bfs_vs_dijkstra.png"),
    },
    "sparse_dense_100": {
        "comparison": Path("plots/sparse_dense_100_time_vs_threads.png"),
    },
    "sparse_dense_big": {
        "comparison": Path("plots/sparse_dense_big_time_vs_threads.png"),
    },
}

THREAD_RE = re.compile(r"^(\d+)\s+Thread", re.IGNORECASE)
TIME_RE = re.compile(r"Computation took:\s*([0-9.]+)\s*seconds", re.IGNORECASE)


def parse_results(path: Path):
    threads = []
    times = []
    current_threads = None

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        match_thread = THREAD_RE.search(line)
        if match_thread:
            current_threads = int(match_thread.group(1))
            continue
        match_time = TIME_RE.search(line)
        if match_time and current_threads is not None:
            threads.append(current_threads)
            times.append(float(match_time.group(1)))
            current_threads = None

    if not threads:
        raise ValueError(f"No timing data found in {path}")

    combined = sorted(zip(threads, times), key=lambda item: item[0])
    threads_sorted, times_sorted = zip(*combined)
    return list(threads_sorted), list(times_sorted)


def plot_time(threads, times, title, output_path: Path):
    plt.figure(figsize=(7, 4.5))
    plt.plot(threads, times, marker="o", linewidth=2)
    plt.title(title)
    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(threads)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_speedup(threads, times, title, output_path: Path):
    base_time = times[0]
    speedup = [base_time / t for t in times]

    plt.figure(figsize=(7, 4.5))
    plt.plot(threads, speedup, marker="o", linewidth=2, color="#2a6f97")
    plt.title(title)
    plt.xlabel("Number of Threads")
    plt.ylabel("Speedup (T1 / Tp)")
    plt.xticks(threads)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()


def parse_single_time(path: Path):
    for raw in path.read_text(encoding="utf-8").splitlines():
        match_time = TIME_RE.search(raw)
        if match_time:
            return float(match_time.group(1))
    raise ValueError(f"No timing data found in {path}")


def plot_library_comparison(cpp_time, nx_time, title, output_path: Path):
    labels = ["Custom C++ (1 Thread)", "Python NetworkX"]
    values = [cpp_time, nx_time]

    plt.figure(figsize=(7, 4.5))
    bars = plt.bar(labels, values, color=["#1b4965", "#5fa8d3"])
    plt.title(title)
    plt.ylabel("Execution Time (seconds)")
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_algorithm_comparison(threads, bfs_times, dijkstra_times, title, output_path: Path):
    plt.figure(figsize=(7, 4.5))
    plt.plot(threads, bfs_times, marker="o", linewidth=2, label="BFS (Unweighted)")
    plt.plot(threads, dijkstra_times, marker="o", linewidth=2, label="Dijkstra (Unweighted)")
    plt.title(title)
    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(threads)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()


def parse_sparse_dense_results(path: Path):
    sections = {}
    current_section = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.lower().startswith("sparse"):
            current_section = "sparse"
            sections[current_section] = []
            continue
        if line.lower().startswith("dense"):
            current_section = "dense"
            sections[current_section] = []
            continue
        match_thread = THREAD_RE.search(line)
        if match_thread:
            sections[current_section].append(int(match_thread.group(1)))
            continue
        match_time = TIME_RE.search(line)
        if match_time and current_section is not None:
            sections[current_section].append(float(match_time.group(1)))

    def split_pairs(values):
        if len(values) % 2 != 0:
            raise ValueError(f"Unexpected sparse/dense format in {path}")
        threads = values[0::2]
        times = values[1::2]
        combined = sorted(zip(threads, times), key=lambda item: item[0])
        threads_sorted, times_sorted = zip(*combined)
        return list(threads_sorted), list(times_sorted)

    if "sparse" not in sections or "dense" not in sections:
        raise ValueError(f"Missing sparse/dense sections in {path}")

    sparse_threads, sparse_times = split_pairs(sections["sparse"])
    dense_threads, dense_times = split_pairs(sections["dense"])
    return sparse_threads, sparse_times, dense_threads, dense_times


def plot_sparse_dense_comparison(threads, sparse_times, dense_times, title, output_path: Path):
    plt.figure(figsize=(7, 4.5))
    plt.plot(threads, sparse_times, marker="o", linewidth=2, label="Sparse")
    plt.plot(threads, dense_times, marker="o", linewidth=2, label="Dense")
    plt.title(title)
    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(threads)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200)
    plt.close()


def main():
    for label, path in RESULT_FILES.items():
        threads, times = parse_results(path)

        plot_time(
            threads,
            times,
            f"Execution Time vs Threads ({label.capitalize()})",
            OUTPUTS[label]["time"],
        )
        plot_speedup(
            threads,
            times,
            f"Speedup Curve ({label.capitalize()})",
            OUTPUTS[label]["speedup"],
        )

        cpp_time = times[0]
        nx_time = parse_single_time(NETWORKX_FILES[label])
        plot_library_comparison(
            cpp_time,
            nx_time,
            f"Library Comparison ({label.capitalize()})",
            OUTPUTS[label]["comparison"],
        )

    unweighted_threads, bfs_times = parse_results(RESULT_FILES["unweighted"])
    dijkstra_threads, dijkstra_times = parse_results(ALGO_COMPARISON_FILE)
    if unweighted_threads != dijkstra_threads:
        raise ValueError("Thread counts do not match for BFS and Dijkstra results")

    plot_algorithm_comparison(
        unweighted_threads,
        bfs_times,
        dijkstra_times,
        "Algorithm Efficiency (Unweighted Dataset)",
        OUTPUTS["algorithm"]["comparison"],
    )

    sparse_100_path = Path("centrality_sparse_dense_100_results.txt")
    sparse_threads, sparse_times, dense_threads, dense_times = parse_sparse_dense_results(
        sparse_100_path
    )
    if sparse_threads != dense_threads:
        raise ValueError("Thread counts do not match for sparse/dense (100)")
    plot_sparse_dense_comparison(
        sparse_threads,
        sparse_times,
        dense_times,
        "Sparse vs Dense (V=100)",
        OUTPUTS["sparse_dense_100"]["comparison"],
    )

    sparse_big_path = Path("centrality_sparse_dense_big_results.txt")
    sparse_threads, sparse_times, dense_threads, dense_times = parse_sparse_dense_results(
        sparse_big_path
    )
    if sparse_threads != dense_threads:
        raise ValueError("Thread counts do not match for sparse/dense (big)")
    plot_sparse_dense_comparison(
        sparse_threads,
        sparse_times,
        dense_times,
        "Sparse vs Dense (Big)",
        OUTPUTS["sparse_dense_big"]["comparison"],
    )

    print("Plots saved to the plots/ directory.")


if __name__ == "__main__":
    main()
