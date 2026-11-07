"""Lab 2 - Task 3: Stateful classroom agent."""



class StatefulClassroomAgent:
    def __init__(self):
        self.previous_mode = None   # no command has been sent yet

    @staticmethod
    def decide(temp, occupied):
        """Pure policy (same as the reflex agent)."""
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"

    def act(self, temp, occupied):
        target = self.decide(temp, occupied)
        send = target != self.previous_mode   # only send when mode changes
        self.previous_mode = target
        return target, send


def run_trace(percepts):
    """Run percepts through a fresh agent; return list of record dicts."""
    agent = StatefulClassroomAgent()
    rows = []
    for step, (temp, occ) in enumerate(percepts, 1):
        prev = agent.previous_mode
        target, send = agent.act(temp, occ)
        rows.append({
            "step": step,
            "previous": prev if prev is not None else "None",
            "percept": (temp, occ),
            "target": target,
            "outcome": "SEND COMMAND" if send else "no command",
        })
    return rows


def print_trace(rows):
    print(f"{'Step':<5}{'Previous':<10}{'Percept':<16}{'Target':<8}Outcome")
    for r in rows:
        print(f"{r["step"]:<5}{r['previous']:<10}{str(r['percept']):<16}"
              f"{r['target']:<8}{r['outcome']}")


if __name__ == "__main__":
    percepts = [
        (29, True),    
        (29, True),    
        (26, True),  
        (20, True),    
        (19, True),    
        (29, False),   
        (15, False),  
    ]
    print_trace(run_trace(percepts))
