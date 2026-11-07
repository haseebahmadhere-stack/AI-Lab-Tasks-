"""Lab 5 - Part 5.1: Plain Minimax with a leaf-evaluation counter.

Tree layout: complete binary tree stored as a flat list of leaf utilities.
Node (depth d, index i) has children (d+1, 2i) and (d+1, 2i+1).
Depth 0 is MAX, depth 1 is MIN, and so on (alternating).
"""
import math


def pad_scores(scores):
    """Pad with 0 up to the next power of two (as in the lab manual).

    NOTE: padding with 0 is NOT neutral - it adds real leaves that can change
    the root value. Prefer trees whose size is already a power of two.
    """
    scores = list(scores)
    depth = math.ceil(math.log2(len(scores))) if len(scores) > 1 else 0
    scores += [0] * (2 ** depth - len(scores))
    return scores, depth


def minimax(depth, index, max_turn, scores, target, counter):
    """Return the Minimax value of node (depth, index).

    counter is a one-element list used as a mutable leaf counter.
    """
    if depth == target:
        counter[0] += 1                      # one leaf evaluated
        return scores[index]

    children = [
        minimax(depth + 1, index * 2 + i, not max_turn, scores, target, counter)
        for i in range(2)
    ]
    return max(children) if max_turn else min(children)


def run_minimax(scores):
    """Convenience wrapper -> (root_value, leaves_evaluated)."""
    scores, depth = pad_scores(scores)
    counter = [0]
    value = minimax(0, 0, True, scores, depth, counter)
    return value, counter[0]


if __name__ == "__main__":
    scores = [3, 5, 2, 9, 0, 7]              # manual example (padded to 8)
    value, leaves = run_minimax(scores)
    print("The optimal value is:", value)
    print("Leaves evaluated    :", leaves)
