"""
Lab 4: Informed Search - Heuristics & A*

Run:  python lab4_astar_audit.py
Uses only the Python standard library.

Conventions (kept identical in every run):
  * Priority queue entries are (f, g, node, path); ties on f are broken by
    smaller g, then alphabetically by node name (heapq tuple ordering).
  * Successors are examined in the order they are listed in the graph.
  * A node counts as "expanded" only when its successors are examined.
    Goal processing is logged but NOT counted.
  * Stale queue entries (g != best[node]) are skipped and logged.
"""
import heapq

GRAPH = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": [],
}
H = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}


def search(graph, h, start, goal, verbose=True):
    """A* (or UCS when h is all zeros). Returns dict with cost, path, trace."""
    pq = [(h[start], 0, start, [start])]
    best = {start: 0}
    expanded, processed, stale = [], [], []
    while pq:
        if verbose:
            snap = sorted(pq)
            print("    frontier:", [(n, "g=%d" % g, "f=%d" % f) for f, g, n, _ in snap])
        f, g, node, path = heapq.heappop(pq)
        if g != best[node]:
            stale.append(node)
            if verbose:
                print(f"  skip stale entry {node} (g={g}, best={best[node]})")
            continue
        processed.append(node)
        if verbose:
            print(f"  pop {node}: g={g} h={h[node]} f={f}")
        if node == goal:
            if verbose:
                print(f"  goal {node} reached (logged, not counted as expansion)")
            return {"cost": g, "path": path, "processed": processed,
                    "expanded": expanded, "stale": stale}
        expanded.append(node)
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))
                if verbose:
                    print(f"    push {nxt}: g={g}+{w}={ng}, h={h[nxt]}, f={ng + h[nxt]}")
            elif verbose:
                print(f"    reject {nxt}: g={g}+{w}={ng} not < best {best[nxt]}")
    return {"cost": None, "path": None, "processed": processed,
            "expanded": expanded, "stale": stale}


def path_cost(graph, path):
    """Independently sum the edge weights along a path."""
    total = 0
    for u, v in zip(path, path[1:]):
        total += dict(graph[u])[v]
    return total


def true_remaining(graph, goal):
    """Exact cost-to-goal for every node (Bellman-Ford style relaxation)."""
    inf = float("inf")
    d = {n: inf for n in graph}
    d[goal] = 0
    for _ in range(len(graph)):
        for u, edges in graph.items():
            for v, w in edges:
                d[u] = min(d[u], w + d[v])
    return d


def audit(graph, h, goal):
    print("Admissibility check: h(n) <= true remaining cost h*(n)")
    hs = true_remaining(graph, goal)
    ok = True
    for n in graph:
        flag = h[n] <= hs[n]
        ok &= flag
        print(f"  {n}: h={h[n]}  h*={hs[n]}  {'OK' if flag else 'OVERESTIMATE'}")
    print("  admissible on this graph:", ok)
    print("Consistency check: h(u) <= cost(u,v) + h(v) for every edge")
    ok2 = True
    for u, edges in graph.items():
        for v, w in edges:
            flag = h[u] <= w + h[v]
            ok2 &= flag
            print(f"  {u}->{v}: {h[u]} <= {w}+{h[v]} = {w + h[v]}  {'OK' if flag else 'FAIL'}")
    print("  consistent:", ok2)


def run(title, graph, h, start, goal):
    print(f"\n=== {title} ===")
    r = search(graph, h, start, goal)
    if r["path"]:
        print(f"  RESULT path={r['path']} returned_cost={r['cost']} "
              f"summed_cost={path_cost(graph, r['path'])}")
    else:
        print("  RESULT no path found")
    print(f"  processed trace : {r['processed']}")
    print(f"  expanded nodes  : {r['expanded']}  (count={len(r['expanded'])})")
    print(f"  stale skips     : {r['stale']}")
    return r


if __name__ == "__main__":
    print("#### Heuristic audit (supplied h) ####")
    audit(GRAPH, H, "G")

    print("\n#### Task 1/2: A* with supplied heuristic ####")
    astar_r = run("A* (supplied h)", GRAPH, H, "S", "G")

    zero = {n: 0 for n in GRAPH}
    ucs_r = run("UCS control (h = 0 everywhere)", GRAPH, zero, "S", "G")

    print("\n#### Comparison table ####")
    print(f"{'Run':<22}{'Path':<20}{'Cost':<6}{'Expanded':<6}  Processed trace")
    for name, r in (("A* (supplied h)", astar_r), ("UCS (h=0)", ucs_r)):
        print(f"{name:<22}{'->'.join(r['path']):<20}{r['cost']:<6}{len(r['expanded']):<6}  {r['processed']}")

    print("\n#### Task 3: overestimate h(C): 2 -> 10 (true remaining = 3) ####")
    h_bad = dict(H)
    h_bad["C"] = 10
    audit(GRAPH, h_bad, "G")
    bad_r = run("A* with h(C)=10", GRAPH, h_bad, "S", "G")

    print("\n#### Extra: overestimate that does NOT change the result: h(B): 4 -> 10 (true=5) ####")
    h_b = dict(H)
    h_b["B"] = 10
    run("A* with h(B)=10", GRAPH, h_b, "S", "G")

    print("\n#### Edge cases ####")
    run("Edge 1: start == goal", GRAPH, H, "G", "G")
    g2 = dict(GRAPH)
    g2["Z"] = []
    h2 = dict(H)
    h2["Z"] = 0
    run("Edge 2: unreachable goal Z", g2, h2, "S", "Z")
