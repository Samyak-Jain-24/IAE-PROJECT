#!/usr/bin/env python3
import re
from pathlib import Path

import matplotlib.pyplot as plt


RESULT_FILES = {
    "unweighted": Path("centrality_results.txt"),
    "weighted": Path("centrality_weighted_results.txt"),
}

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

    print("Plots saved to the plots/ directory.")


if __name__ == "__main__":
    main()
