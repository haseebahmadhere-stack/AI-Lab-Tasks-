"""
Lab 3 - Task 2: Depth-Limited Search (DLS) and Iterative Deepening DFS (IDDFS)

"""
FOUND, CUTOFF, FAILURE = "FOUND", "CUTOFF", "FAILURE"

graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"],
         "D": [], "E": ["G"], "F": [], "G": []}


def dls(g, start, goal, limit):
    """Returns (status, path, processed_order)."""
    order = []

    def rec(node, path, lim):
        order.append(node)
        if node == goal: return FOUND, list(path)
        children = [n for n in g[node] if n not in path]   # path-local cycle check
        if lim == 0:
            return (CUTOFF, None) if children else (FAILURE, None)
        cutoff = False
        for n in children:
            status, res = rec(n, path + [n], lim - 1)
            if status == FOUND: return FOUND, res
            if status == CUTOFF: cutoff = True
        return (CUTOFF, None) if cutoff else (FAILURE, None)

    status, path = rec(start, [start], limit)
    return status, path, order


def iddfs(g, start, goal, max_depth):
    """Returns (status, path, limits_attempted, total_nodes_processed)."""
    attempted, total = [], 0
    for limit in range(0, max_depth + 1):
        attempted.append(limit)
        status, path, order = dls(g, start, goal, limit)
        total += len(order)
        if status == FOUND: return FOUND, path, attempted, total
        if status == FAILURE: return FAILURE, None, attempted, total   # whole graph exhausted
    return CUTOFF, None, attempted, total


def buggy_dls_global_visited(g, start, goal, limit):
    """DEMO OF THE WRONG WAY: one global visited set shared across branches."""
    visited = set()

    def rec(node, path, lim):
        if node == goal: return path
        visited.add(node)
        if lim == 0: return None
        for n in g[node]:
            if n not in visited:
                r = rec(n, path + [n], lim - 1)
                if r: return r
        return None
    return rec(start, [start], limit)


if __name__ == "__main__":
    print("=== DLS on original graph (A -> G) ===")
    for lim in (1, 2, 3, 4):
        s, p, o = dls(graph, "A", "G", lim)
        print(f"limit={lim}: status={s:<8} path={p} processed={o} ({len(o)} nodes)")

    print("\n=== IDDFS on original graph (A -> G) ===")
    for md in (1, 2, 3, 4):
        s, p, att, tot = iddfs(graph, "A", "G", md)
        print(f"max_depth={md}: status={s:<8} path={p} limits_attempted={att} total_nodes_processed={tot}")

    print("\n=== Edge-case tests ===")
    print("Start == goal  DLS(limit 0):", dls(graph, "A", "A", 0)[:2])
    g2 = dict(graph); g2["H"] = []
    print("Unreachable H, DLS limit 10:", dls(g2, "A", "H", 10)[:2], "(whole graph exhausted)")
    print("Unreachable H, DLS limit 2 :", dls(g2, "A", "H", 2)[:2], "(only bounded result, NOT proof)")
    print("Unreachable H, IDDFS max 10:", iddfs(g2, "A", "H", 10)[:3])
    cyc = {"A": ["B"], "B": ["A", "C"], "C": ["B"], "Z": []}
    print("Cycle graph, goal Z, DLS limit 10:", dls(cyc, "A", "Z", 10)[:2], "(terminates, no infinite loop)")
    print("Cycle graph, goal C, IDDFS max 5 :", iddfs(cyc, "A", "C", 5))

    print("\n=== Failure case: global visited set across branches (WRONG) vs path-local (RIGHT) ===")
    dia = {"A": ["B", "C"], "B": ["C"], "C": ["D"], "D": ["G"], "G": []}
    print("Graph:", dia, "| goal G needs A->C->D->G (depth 3)")
    print("Global visited, limit 3:", buggy_dls_global_visited(dia, "A", "G", 3))
    print("Path-local    , limit 3:", dls(dia, "A", "G", 3)[:2])
