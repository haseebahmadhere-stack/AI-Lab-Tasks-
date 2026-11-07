"""
Lab 3 - Task 1: BFS and DFS (supplied code + traced versions)

"""
from collections import deque

# ---------- Original graph from Section 3.2 (successor order = tie-break order)
graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"],
         "D": [], "E": ["G"], "F": [], "G": []}


# ---------- Supplied code (unchanged logic) ----------
def bfs(start, goal, g=graph):
    q = deque([(start, [start])]); seen = {start}
    while q:
        node, path = q.popleft()
        if node == goal: return path
        for n in g[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))


def dfs(start, goal, g=graph):
    stack = [(start, [start])]; seen = set()
    while stack:
        node, path = stack.pop()
        if node == goal: return path
        if node in seen: continue
        seen.add(node)
        for n in reversed(g[node]): stack.append((n, path + [n]))


# ---------- Traced versions (print frontier after every step) ----------
def bfs_trace(start, goal, g=graph, verbose=True):
    q = deque([(start, [start])]); seen = {start}; order = []; step = 0
    if verbose: print(f"{'Step':<5}{'Processed':<11}{'Path':<14}Queue after step")
    while q:
        node, path = q.popleft(); step += 1; order.append(node)
        if node == goal:
            if verbose: print(f"{step:<5}{node:<11}{'->'.join(path):<14}GOAL FOUND")
            return path, order
        for n in g[node]:
            if n not in seen:
                seen.add(n); q.append((n, path + [n]))
        if verbose:
            print(f"{step:<5}{node:<11}{'->'.join(path):<14}{[x for x, _ in q]}")
    return None, order


def dfs_trace(start, goal, g=graph, verbose=True):
    stack = [(start, [start])]; seen = set(); order = []; step = 0
    if verbose: print(f"{'Step':<5}{'Processed':<11}{'Path':<14}Stack after step (bottom -> top)")
    while stack:
        node, path = stack.pop(); step += 1
        if node == goal:
            order.append(node)
            if verbose: print(f"{step:<5}{node:<11}{'->'.join(path):<14}GOAL FOUND")
            return path, order
        if node in seen:
            if verbose: print(f"{step:<5}{node:<11}{'->'.join(path):<14}(duplicate, skipped)")
            continue
        seen.add(node); order.append(node)
        for n in reversed(g[node]): stack.append((n, path + [n]))
        if verbose:
            print(f"{step:<5}{node:<11}{'->'.join(path):<14}{[x for x, _ in stack]}")
    return None, order


if __name__ == "__main__":
    print("=== Supplied code output ===")
    print(bfs("A", "G")); print(dfs("A", "G"))

    print("\n=== BFS trace (A -> G) ===")
    p, o = bfs_trace("A", "G")
    print("Final path :", p); print("Visit order:", o, f"({len(o)} nodes processed incl. goal)")

    print("\n=== DFS trace (A -> G) ===")
    p, o = dfs_trace("A", "G")
    print("Final path :", p); print("Visit order:", o, f"({len(o)} nodes processed incl. goal)")

    print("\n=== Edge-case tests ===")
    print("Start == goal  BFS:", bfs("A", "A"), "| DFS:", dfs("A", "A"))
    g2 = dict(graph); g2["H"] = []
    print("Unreachable H  BFS:", bfs("A", "H", g2), "| DFS:", dfs("A", "H", g2))
    cyc = {"A": ["B"], "B": ["A", "C"], "C": []}
    print("Cycle graph A->C  BFS:", bfs("A", "C", cyc), "| DFS:", dfs("A", "C", cyc))
    print("Cycle graph, goal Z (unreachable)  BFS:", bfs("A", "Z", {**cyc, "Z": []}),
          "| DFS:", dfs("A", "Z", {**cyc, "Z": []}), "(terminates: no infinite loop)")
