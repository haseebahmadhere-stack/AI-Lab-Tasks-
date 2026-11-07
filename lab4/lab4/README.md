# Lab 4: Informed Search - Heuristics & A*

- **Course:** CAI601400 - Artificial Intelligence Lab
- **Student:** Haseeb Ahmad
- **Roll No:** 057
- **Semester / Section:** 3A
- **Instructor:** Rasikh Ali

## Contents

| File | Purpose |
|---|---|
| `lab4_astar_audit.py` | A* / UCS implementation, heuristic audit, overestimate experiment, edge cases |
| `output_log.txt` | Captured output of the script (full traces) |
| `Lab4_Report.docx` | Written report (manual g/h/f calculations, audit, comparison, experiments, reflection) |
| `README.md` | This file |

## Setup

- Python 3.8 or newer. No third-party packages are needed (only `heapq` from the standard library).
- No credentials, private data or virtual environments are included.

## Run

```bash
cd lab4
python lab4_astar_audit.py
# to regenerate the captured output:
python lab4_astar_audit.py > output_log.txt
```

## Conventions used (identical in every run)

- Queue entries are `(f, g, node, path)`; ties on `f` are broken by smaller `g`, then node name.
- Successors are examined in the order listed in the graph.
- A node is counted as *expanded* only when its successors are examined. Goal processing is logged but not counted.
- Stale queue entries (`g != best[node]`) are skipped and logged.

## Graph and heuristic

Edges (travel-time units): S->A 1, S->B 4, A->C 2, B->G 5, C->G 3.
Heuristic: h(S)=5, h(A)=4, h(B)=4, h(C)=2, h(G)=0 (abstract time estimates, not measured distances).

## Expected key results

| Run | Path | Cost | Expanded nodes |
|---|---|---|---|
| A* (supplied h) | S-A-C-G | 6 | 3 (S, A, C) |
| UCS (h = 0) | S-A-C-G | 6 | 4 (S, A, C, B) |
| A* with h(C)=10 | S-B-G | 9 (not optimal) | 3 (S, A, B) |

## Source note

The base A* code follows the guided implementation in the CAI601400 Lab 4 manual (Section 4.2); it was extended with tracing, expansion counting, stale-entry logging and audit functions.
