"""Lab 2 - self-checks, reflex vs stateful comparison and edge case test."""


from lab2_percepts import ClassroomAgent
from lab2_model import StatefulClassroomAgent, run_trace, print_trace


def check_reflex():
    a = ClassroomAgent()
    percepts = [(29, True), (29, True), (20, True),
                (26, True), (19, True), (29, False)]
    got = [a.act(*p) for p in percepts]
    expected = ["COOL", "COOL", "IDLE", "IDLE", "WARM", "ECO"]
    assert got == expected, (got, expected)
    print("PASS reflex agent matches expected modes:", got)


def check_stateful():
    a = StatefulClassroomAgent()
    assert a.act(29, True) == ("COOL", True)    
    assert a.act(29, True) == ("COOL", False)   
    assert a.act(26, True) == ("IDLE", True)    
    assert a.act(20, True) == ("IDLE", False)   
    assert a.act(19, True) == ("WARM", True)    
    assert a.act(29, False) == ("ECO", True)    
    assert a.act(15, False) == ("ECO", False)   
    print("PASS stateful agent: repeats, boundaries, transition, empty room")


def check_same_targets():
    """Stateful agent must pick the same target as the reflex agent."""
    r, s = ClassroomAgent(), StatefulClassroomAgent()
    for t in range(10, 40):
        for occ in (True, False):
            assert r.act(t, occ) == s.act(t, occ)[0]
    print("PASS stateful targets identical to reflex targets (10-39 C)")


def compare_reflex_vs_stateful():
    percepts = [(29, True)] * 4 + [(24, True)] * 3 + [(29, False)] * 2
    r = ClassroomAgent()
    reflex_cmds = sum(1 for p in percepts if r.act(*p))   # sends every step
    rows = run_trace(percepts)
    stateful_cmds = sum(1 for x in rows if x["outcome"] == "SEND COMMAND")
    print(f"Comparison on {len(percepts)} percepts: reflex sends "
          f"{reflex_cmds} commands, stateful sends {stateful_cmds}")
    assert stateful_cmds < reflex_cmds


def edge_case_noisy_26():
    """Noisy readings around 26 C: memory alone does not give hysteresis."""
    print("\nEdge case - noisy sequence around 26 C (occupied room):")
    noisy = [25.9, 26.1, 25.9, 26.1, 25.9, 26.1]
    rows = run_trace([(t, True) for t in noisy])
    print_trace(rows)
    sent = sum(1 for x in rows if x["outcome"] == "SEND COMMAND")
    print(f"Commands sent: {sent} of {len(noisy)} (rapid IDLE/COOL flipping)")
    assert sent == len(noisy)   # every step flips -> no hysteresis


if __name__ == "__main__":
    check_reflex()
    check_stateful()
    check_same_targets()
    compare_reflex_vs_stateful()
    edge_case_noisy_26()
    print("\nALL CHECKS PASSED")
