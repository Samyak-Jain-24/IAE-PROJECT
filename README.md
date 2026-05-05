# Closeness Centrality (C++ OpenMP)

Arnav Agnihotri - 2024101103
Samyak Jain - 2024101062

NOTE : WE HAVE REMOVED SOME OF THE LARGE DATASETS AS THEY WERE BEEN TOO MUCH MEMORY TAKING AND WERE NOT BEEN ABLE TO BE PUSHED ON GITHUB AND MOODLE
GOOGLE DRIVE DATASET LINK - https://drive.google.com/drive/folders/1Qdc-3Y4ITboTQsiGg2yR53ODQ8ur---C?usp=sharing

## Overview
This project computes closeness centrality for unweighted and weighted graphs using a parallel C++ (OpenMP) implementation. It also includes Python/NetworkX baselines and plotting scripts for performance analysis.

## Project Structure
- centrality: C++ executable (built)
- centrality.exe: Alternative build output (if present)
- graph.hpp / graph.cpp: Graph data structure and shortest-path routines
- main.cpp: C++ driver for closeness centrality
- compare.py: NetworkX baseline (unweighted or weighted)
- compare_weighted.py: NetworkX baseline for weighted graphs
- make_plots.py: Generates performance plots
- data/: Input datasets
  - unweighted.txt
  - weighted.txt
  - wiki-Vote.txt/Wiki-Vote.txt
  - wiki-Vote-weighted.txt
- centrality_results.txt: Timing results for unweighted dataset
- centrality_weighted_results.txt: Timing results for weighted dataset
- networkx_time.txt: NetworkX timing result (unweighted)
- networkx_weighted_time.txt: NetworkX timing result (weighted)
- plots/: Generated charts

## Build
Requires a C++20 compiler with OpenMP support.

```bash
make
```

## Run (C++)
Usage:

```bash
./centrality <filename> <is_weighted (0 or 1)>
```

Examples:

```bash
./centrality data/wiki-Vote.txt/Wiki-Vote.txt 0
./centrality data/wiki-Vote-weighted.txt 1
```

Set threads with OpenMP:

```bash
export OMP_NUM_THREADS=8
./centrality data/wiki-Vote.txt/Wiki-Vote.txt 0
```

## Run (NetworkX Baseline)
Install dependency:

```bash
pip install networkx
```

Unweighted or weighted (single script):

```bash
python3 compare.py data/wiki-Vote.txt/Wiki-Vote.txt 0
python3 compare_weighted.py data/wiki-Vote-weighted.txt 1
```

Weighted-only script:

```bash
python3 compare_weighted.py data/wiki-Vote-weighted.txt 1
```

## Generate Plots
This script reads the timing files and produces:
- Execution time vs threads (unweighted, weighted)
- Speedup curves (unweighted, weighted)
- C++ vs NetworkX comparison (unweighted, weighted)
- BFS vs Dijkstra (unweighted dataset)

```bash
python3 make_plots.py
```

Outputs are saved in the plots/ directory.

## Notes
- The unweighted implementation uses BFS; the weighted implementation uses Dijkstra.
- The algorithm-efficiency plot uses an additional timing file for running Dijkstra on the unweighted dataset. Update the path in make_plots.py if that file is stored elsewhere.
0-unweighted
1-weighted

## Clean

```bash
make clean
```