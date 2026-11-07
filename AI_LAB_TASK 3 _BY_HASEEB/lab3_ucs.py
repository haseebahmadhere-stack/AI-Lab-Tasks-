
import heapq
from collections import deque

# node -> list of (neighbour, cost); list order = tie-break order
wgraph = {
    "A": [("B", 1), ("C", 5)],
    "B": [("D", 2), ("E", 1)],
    "C": [("F", 3), ("G", 7)],   # C->G is the ADDED corridor (cost 7)
    "D": [], "E": [("G", 1)], "F": [], "G": [],
}


def ucs(g, start, goal):
    """Returns (path, cost, processed_order). Ties broken by insertion order (counter)."""
    for u in g:
        for v, w in g[u]:
            if w < 0: raise ValueError(f"Negative edge {u}->{v}={w}: UCS requires nonnegative costs")
    tick = 0
    pq = [(0, tick, start, [start])]; best = {start: 0}; done = set(); order = []
    while pq:
        cost, _, node, path = heapq.heappop(pq)
        if node in done: continue            # stale queue entry
        done.add(node); order.append((node, cost))
        if node == goal: return path, cost, order
        for n, w in g[node]:
            nc = cost + w
            if n not in done and nc < best.get(n, float("inf")):
                best[n] = nc; tick += 1
                heapq.heappush(pq, (nc, tick, n, path + [n]))
    return None, float("inf"), order


def bfs_hops(g, start, goal):
    """BFS ignoring weights (fewest edges). Returns (path, processed_order)."""
    q = deque([(start, [start])]); seen = {start}; order = []
    while q:
        node, path = q.popleft(); order.append(node)
        if node == goal: return path, order
        for n, _ in g[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))
    return None, order


def path_cost(g, path):
    """Independent verification: sum edge weights along a path."""
    total, parts = 0, []
    for a, b in zip(path, path[1:]):
        w = dict(g[a])[b]; total += w; parts.append(str(w))
    return total, " + ".join(parts) if parts else "0"


if __name__ == "__main__":
    print("=== Weighted graph (edge: cost) ===")
    for u, es in wgraph.items():
        for v, w in es:
            print(f"  {u} -> {v} : {w}" + ("   <-- ADDED corridor" if (u, v) == ("C", "G") else ""))

    print("\n=== UCS A -> G ===")
    p, c, o = ucs(wgraph, "A", "G")
    print("Processing order (node, g-cost):", o)
    print("Path:", p, "| UCS reported cost:", c, "| hops:", len(p) - 1)
    t, expr = path_cost(wgraph, p)
    print(f"Independent edge-sum: {expr} = {t}   (matches: {t == c})")

    print("\n=== BFS (fewest edges) on same weighted topology ===")
    bp, bo = bfs_hops(wgraph, "A", "G")
    print("Processing order:", bo)
    bt, bexpr = path_cost(wgraph, bp)
    print("Path:", bp, "| hops:", len(bp) - 1, f"| cost: {bexpr} = {bt}")

    print("\n=== Comparison ===")
    print(f"BFS : {len(bp)-1} hops, cost {bt}")
    print(f"UCS : {len(p)-1} hops, cost {c}")
    print("Fewest hops != lowest cost: BFS minimises edge count only; UCS minimises total cost.")

    print("\n=== Edge-case tests ===")
    print("Start == goal :", ucs(wgraph, "A", "A"))
    g2 = {**wgraph, "H": []}
    print("Unreachable H :", ucs(g2, "A", "H")[:2])
    cyc = {"A": [("B", 1)], "B": [("A", 1), ("C", 2)], "C": [("B", 2)]}
    print("Cycle graph A->C:", ucs(cyc, "A", "C"))
    try:
        ucs({"A": [("B", -1)], "B": []}, "A", "B")
    except ValueError as e:
        print("Negative edge :", e)
