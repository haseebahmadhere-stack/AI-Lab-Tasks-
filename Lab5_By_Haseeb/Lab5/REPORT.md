# Lab 5: Adversarial Search - Minimax & Alpha-Beta Pruning

Course: CAI601400 - Artificial Intelligence Lab | CLO2 (C3: Apply) | Student: Rasikh Ali - 42365

 1. Objective
Apply Minimax and Alpha-Beta pruning to a game tree, show that pruning keeps the Minimax decision, and measure how many leaves each algorithm evaluates.

 2. Folder contents
| File | Purpose |
|---|---|
| `minimax.py` | Plain Minimax with a leaf counter (Lab Task 2) |
| `alphabeta.py` | Alpha-Beta with a leaf counter and a pruning trace |
| `experiments.py` | Comparison, branch reordering, edge cases, 500 random trees (Lab Task 3) |
| `output.txt` | Captured output of all three scripts |
| `REPORT.md` | This report (trace, interpretation, viva, reflection) |

Run: `python3 experiments.py` (it imports the other two files and asserts correctness).

 3. Hand trace (Lab Task 1)
Tree layout: depth 0 = MAX, depth 1 = MIN, depth 2 = MAX, depth 3 = leaves. Node (d, i) has children (d+1, 2i) and (d+1, 2i+1).

#3.1 Minimax on the manual tree `[3, 5, 2, 9, 0, 7]`
The lab pads with zeros to 8 leaves: `[3, 5, 2, 9, 0, 7, 0, 0]`.

| Level | Node | Computation | Value |
|---|---|---|---|
| MAX (d2) | A | max(3, 5) | 5 |
| MAX (d2) | B | max(2, 9) | 9 |
| MAX (d2) | C | max(0, 7) | 7 |
| MAX (d2) | D | max(0, 0) | 0 |
| MIN (d1) | L | min(5, 9) | 5 |
| MIN (d1) | R | min(7, 0) | 0 |
| MAX (root) | root | max(5, 0) | **5** |

Best action: go left (toward L). Program output: `The optimal value is: 5` using 8 leaves.

# 3.2 Alpha-Beta on `[3, 5, 2, 9, 3, 5, 2, 9]`
Initial call: alpha = -inf, beta = +inf.

1. Root (MAX) enters left MIN node L. Leaves 3, 5 give MAX node = 5, so L's beta = 5. Leaves 2, 9 give 9, so L = min(5, 9) = **5**.
2. Back at the root: alpha = max(-inf, 5) = 5.
3. Root enters right MIN node R with alpha = 5. Its first child MAX(3, 5) = 5, so R's beta = 5.
4. Now alpha (5) >= beta (5): **prune**. The second child of R (leaves 2, 9) is never evaluated. R can only be <= 5, so it cannot beat the 5 MAX already has.
5. Root = max(5, 5) = **5**.

Leaves evaluated: 6 of 8. The program's trace prints exactly this: `PRUNE under MIN node (d=1, i=1): alpha=5 >= beta=5`.

4. Results (from `output.txt`)

# 4.1 Supplied trees
| Tree | Minimax | Alpha-Beta | Leaves MM | Leaves AB |
|---|---|---|---|---|
| `[3,5,2,9,3,5,2,9]` | 5 | 5 | 8 | 6 |
| `[3,5,2,9,0,7,0,0]` | 5 | 5 | 8 | 8 |

The second tree gets no pruning at all, so pruning is not guaranteed; it depends on the leaf order and values.

# 4.2 Reordering branches (Lab Task 3)
Same leaves as `[3,5,2,9,3,5,2,9]`, different order:

| Ordering | Root value | Leaves MM | Leaves AB |
|---|---|---|---|
| Original | 5 | 8 | 6 |
| Swap leaf pairs | 5 | 8 | "5" |
| Swap subtrees (block = 2) | 5 | 8 | "8" |
| Swap halves (block = 4) | 5 | 8 | 6 |
| Swap pairs + subtrees | 5 | 8 | 8 |
| 16 leaves, descending order | 5 | 16 | 8 |
| 16 leaves, ascending order | 5 | 16 | 12 |

"Why the counts differ (two checked by hand):"
- *Swap leaf pairs* (`[5,3,9,2,5,3,9,2]`): in the left MIN node, the first MAX child gives 5, so beta = 5. The second MAX child sees leaf 9 >= beta, so leaf 2 is skipped. The right MIN node is pruned after its first child as before. Total 3 + 2 = 5 leaves.
- *Swap subtrees* (`[2,9,3,5,2,9,3,5]`): the right MIN node's first child evaluates to 9, which is higher than alpha = 5, so MIN has not yet found a value low enough to cut anything. No pruning, 8 leaves.

Key observation: the root value is 5 every time; only the work changes.

### 4.3 Edge cases
| Case | Minimax | Alpha-Beta | Leaves MM / AB |
|---|---|---|---|
| Single leaf `[7]` | 7 | 7 | 1 / 1 |
| Two leaves `[4, 8]` | 8 | 8 | 2 / 2 |
| All equal `[5]*8` | 5 | 5 | 8 / 5 |
| All negative | -3 | -3 | 8 / 7 |
| Very large +/- values | 3 | 3 | 8 / 7 |

Note: with all-equal leaves pruning still triggers, because the condition is `alpha >= beta` (equal counts).

### 4.4 Random test
500 random depth-4 trees (16 leaves, values -20..20, seed 42): root values were identical in all 500 cases and Alpha-Beta never evaluated more leaves than Minimax. Average leaves: Minimax 16.00, Alpha-Beta 11.84 (about 26% fewer).

## 5. Interpretation (link to learning outcome)
- Alpha-Beta returns the same Minimax value because it only skips branches that provably cannot change the decision at the root.
- Savings come from move ordering: pruning is strong when the first branch explored at a MAX node is high and at a MIN node is low. In the best case alpha-beta searches about b^(d/2) leaves instead of b^d.
- In the worst ordering it degrades to plain Minimax (8 of 8 above) but never does more work (verified by assertion on every test).

## 6. Limitations / failure analysis
- **Zero padding is not neutral.** The lab's Minimax code pads leaves with 0 to reach a power of two. This adds fake leaves and can change the root value (e.g. `[3,5,2,9,0,7]` becomes `[3,5,2,9,0,7,0,0]`). Use trees whose size is already 2^k when comparing algorithms.
- The code only handles complete binary trees; real games have varying branching and need a depth limit plus an evaluation function.
- The 500-tree average is for random orderings; real games with good ordering heuristics prune far more.

## 7. Viva-ready answers
- **Why does MAX assume MIN plays the worst move for MAX?** In a zero-sum game, MIN's gain is MAX's loss, so an optimal opponent minimizes MAX's utility; MAX plans for that guaranteed outcome.
- **What are alpha and beta?** Alpha is the best value MAX can already guarantee along the current path; beta is the best value MIN can already guarantee. Prune when alpha >= beta.
- **Does pruning change the result?** No. The root value and best action are identical; only unnecessary leaves are skipped.
- **Why does move ordering matter?** Early good moves tighten alpha/beta sooner, so more later branches get cut (see 5 leaves vs 8 leaves above for the same tree).
- **Design choices:** a list-based complete binary tree for simplicity, a mutable counter list to count leaves without global variables, and asserts so every run proves correctness.

## 8. Reflection
- **What did I learn?** Pruning saves work without changing the answer, and the amount saved depends heavily on ordering.
- **Real-AI application:** game engines (chess, Go) use alpha-beta with move-ordering heuristics and depth-limited evaluation.
- **What surprised me?** Swapping subtrees alone took Alpha-Beta from 6 leaves to 8, so pruning can vanish with the same data. Also, the lab's zero padding silently changes the tree.
- **Do differently next time:** add a depth-limited version with an evaluation function and try a simple move-ordering heuristic on a real game such as tic-tac-toe.

## 9. Responsible practice (transparency)
All trees, utilities, pruning decisions and counters are printed in `output.txt` so another student can reproduce the chosen move and every leaf count.
