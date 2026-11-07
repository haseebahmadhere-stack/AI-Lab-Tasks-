"""Lab 5 - Experiments: comparison, reordering, edge cases, random check."""
import random
from minimax import run_minimax
from alphabeta import run_alphabeta


def swap_children(scores, block):
    """Swap every pair of adjacent blocks of size `block` (reorders branches)."""
    out = list(scores)
    for s in range(0, len(out), 2 * block):
        out[s:s + block], out[s + block:s + 2 * block] = (
            out[s + block:s + 2 * block], out[s:s + block])
    return out


def compare(name, scores):
    mm_v, mm_n = run_minimax(scores)
    ab_trace = []
    ab_v, ab_n = run_alphabeta(scores, ab_trace)
    ok = (mm_v == ab_v) and (ab_n <= mm_n)
    print(f"{name:<34} minimax={mm_v:<4} alphabeta={ab_v:<4} "
          f"leaves MM={mm_n:<3} AB={ab_n:<3} {'OK' if ok else 'FAIL'}")
    assert ok, f"Mismatch in {name}"
    return ab_trace


print("=" * 90)
print("TEST 1: Supplied trees")
print("=" * 90)
manual_ab = [3, 5, 2, 9, 3, 5, 2, 9]
trace = compare("Manual alpha-beta tree (8 leaves)", manual_ab)
for t in trace:
    print("    ", t)
compare("Manual minimax tree [3,5,2,9,0,7,0,0]", [3, 5, 2, 9, 0, 7, 0, 0])

print()
print("=" * 90)
print("TEST 2: Reordering branches (value must stay the same)")
print("=" * 90)
base = [3, 5, 2, 9, 3, 5, 2, 9]
compare("Original order", base)
compare("Swap leaf pairs", swap_children(base, 1))
compare("Swap subtrees (block=2)", swap_children(base, 2))
compare("Swap halves (block=4)", swap_children(base, 4))
compare("Swap pairs + subtrees", swap_children(swap_children(base, 1), 2))

# Hand-built best case / worst case for 16 leaves
best = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5]
worst = list(reversed(best))
compare("16 leaves, good ordering", best)
compare("16 leaves, bad ordering", worst)

print()
print("=" * 90)
print("TEST 3: Edge cases")
print("=" * 90)
compare("Single leaf", [7])
compare("Two leaves", [4, 8])
compare("All equal leaves", [5] * 8)
compare("All negative leaves", [-3, -9, -1, -7, -4, -2, -8, -6])
compare("Contains +inf/-inf-like extremes", [10**9, -10**9, 0, 1, 2, 3, 4, 5])

print()
print("=" * 90)
print("TEST 4: 500 random trees (depth 4, 16 leaves)")
print("=" * 90)
random.seed(42)
tot_mm = tot_ab = 0
for _ in range(500):
    leaves = [random.randint(-20, 20) for _ in range(16)]
    mm_v, mm_n = run_minimax(leaves)
    ab_v, ab_n = run_alphabeta(leaves)
    assert mm_v == ab_v and ab_n <= mm_n
    tot_mm += mm_n
    tot_ab += ab_n
print(f"All 500 trees: root values identical, alpha-beta never used more leaves.")
print(f"Average leaves  Minimax={tot_mm / 500:.2f}  Alpha-Beta={tot_ab / 500:.2f}  "
      f"(saved {100 * (1 - tot_ab / tot_mm):.1f}%)")
