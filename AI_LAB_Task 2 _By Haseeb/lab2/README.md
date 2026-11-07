# Lab 2: Intelligent Agents & the PEAS Framework

- **Course:** CAI601400 - Artificial Intelligence Lab
- **Student:** Haseeb Ahmad
- **Roll No:** SU92-BSAIM-F25-057
- **Semester / Section:** 3 / A
- **Instructor:** Rasikh Ali

## Contents

| File | Purpose |
|---|---|
| "lab2_percepts.py" | Reflex classroom agent and the 6-step percept/action trace (Section 2.5) |
| "lab2_model.py" | Task 3: stateful agent that remembers the previous mode and returns `(target, send_command)` |
| "lab2_check.py" | Assertions, reflex-vs-stateful comparison and the noisy-26 C edge case |
| "outputs/"| Captured outputs of all three scripts |
| "Lab2_Report.docx" | Full report: PEAS specs, classification, comparison, trace, edge case, reflection |

## Setup

Python 3.8+ is required. No external packages and no virtual environment are needed.

```
python --version
```

## Run

```
python lab2_percepts.py
python lab2_model.py
python lab2_check.py
```

`lab2_check.py` exits with an error if any check fails and prints `ALL CHECKS PASSED` otherwise.

## Notes

- Temperature is in degrees Celsius; "occupied" is a Boolean.
- ECO, COOL, WARM and IDLE are simulated mode labels; no hardware is controlled.
- An empty room has priority over temperature. At exactly 20 C or 26 C an occupied room is IDLE.
- The stateful agent is not learning and does not provide hysteresis (see the report, Section 6).
- No credentials, private data or virtual environments are included.
