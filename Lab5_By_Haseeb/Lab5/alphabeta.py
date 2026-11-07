"""Lab 5 - Part 5.2: Alpha-Beta pruning with a leaf-evaluation counter.

alpha = best value MAX can already guarantee on the path to the root.
beta  = best value MIN can already guarantee on the path to the root.
Prune when alpha >= beta: the opponent would never allow this branch.
"""
import math


def alphabeta(depth, index, max_turn, scores, target, alpha, beta, counter,
              trace=None):
    if depth == target:
        counter[0] += 1
        return scores[index]

    if max_turn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta(depth + 1, index * 2 + i, False,
                                         scores, target, alpha, beta,
                                         counter, trace))
            alpha = max(alpha, value)
            if alpha >= beta:
                if trace is not None and i == 0:
                    trace.append(f"PRUNE under MAX node (d={depth}, i={index}): "
                                 f"alpha={alpha} >= beta={beta}")
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            value = min(value, alphabeta(depth + 1, index * 2 + i, True,
                                         scores, target, alpha, beta,
                                         counter, trace))
            beta = min(beta, value)
            if alpha >= beta:
                if trace is not None and i == 0:
                    trace.append(f"PRUNE under MIN node (d={depth}, i={index}): "
                                 f"alpha={alpha} >= beta={beta}")
                break
        return value


def run_alphabeta(scores, trace=None):
    """Convenience wrapper -> (root_value, leaves_evaluated).

    Scores must already be a power of two in length.
    """
    depth = int(math.log2(len(scores))) if len(scores) > 1 else 0
    counter = [0]
    value = alphabeta(0, 0, True, scores, depth,
                      float('-inf'), float('inf'), counter, trace)
    return value, counter[0]


if __name__ == "__main__":
    scores = [3, 5, 2, 9, 3, 5, 2, 9]        # manual example
    trace = []
    value, leaves = run_alphabeta(scores, trace)
    print("Alpha-beta value   :", value)
    print("Leaves evaluated   :", leaves, "of", len(scores))
    for line in trace:
        print(" ", line)
