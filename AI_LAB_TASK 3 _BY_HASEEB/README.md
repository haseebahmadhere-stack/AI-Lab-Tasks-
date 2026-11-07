# Lab 3 – Uninformed Search: BFS, DFS, DLS, IDDFS & UCS



## Folder contents
| File | Purpose |
|---|---|
| "lab3_bfs_dfs.py" | Task 1 – supplied BFS/DFS + traced versions (frontier printed each step) + edge cases |
| `lab3_depth_search.py` | Task 2 – DLS (FOUND/CUTOFF/FAILURE, path-local cycle check) + IDDFS + edge cases + global-visited failure demo |
| `lab3_ucs.py` | Task 3 – weighted graph, UCS with priority queue, BFS comparison, independent cost check, edge cases |
| `outputs/bfs_dfs_output.txt` | Captured output of Task 1 |
| `outputs/depth_search_output.txt` | Captured output of Task 2 |
| `outputs/ucs_output.txt` | Captured output of Task 3 |
| `Lab3_Report.docx` | Full report (assumptions, manual traces, results, failure analysis, reflection) |

## Setup
Python 3.8+ only. No external packages, no virtual environment needed.

## Run
```bash
python lab3_bfs_dfs.py
python lab3_depth_search.py
python lab3_ucs.py
```
To regenerate the captured outputs:
```bash
python lab3_bfs_dfs.py      > outputs/bfs_dfs_output.txt
python lab3_depth_search.py > outputs/depth_search_output.txt
python lab3_ucs.py          > outputs/ucs_output.txt
```

## Conventions
- Successor-list order is the tie-breaking order (left-to-right).
- A node is *processed* when removed from the queue/stack; the goal is counted.
- Depth counts edges; root A has depth 0.
- Weighted experiment adds the corridor **C → G (cost 7)**; it is not in the original trace graph.
  Weights: A-B 1, A-C 5, B-D 2, B-E 1, C-F 3, C-G 7, E-G 1 (all nonnegative).

## Sources
Graph, supplied BFS/DFS code and task requirements: *CAI601400 AI Lab Manual, Lab 3* (instructor Rasikh Ali).
DLS, IDDFS and UCS were written by me following the lecture descriptions (Lectures L5–L6).
