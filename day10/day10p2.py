import os
from collections import deque

class MachineDescr:
    def __init__(self, s: str):
        s = s.strip()
        i = s.index("]")
        self.lights = [c == '#' for c in s[1:i]]

        j = s.index("{")
        self.wirings = [[int(strnum) for strnum in parens[1:-1].split(",")] for parens in s[i+1:j].split()]

        self.counters = [int(strnum) for strnum in s[j+1:-1].split(",")]

    def __repr__(self):
        return f"(lights:{self.lights} wiring:{self.wirings} counters:{self.counters})"


with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [MachineDescr(line) for line in file]

# initially the counters are all zero
# pressing a button toggles increments wired counters by one
# we want to get counters to given state

# doing the bfs takes too much time
#
# actually, there is no difference in which order we press the buttons 
# we only need to find how many times to press each button
#
# checking all possible numbers of presses also takes too many time


def solve(machine: MachineDescr) -> int:
    # do the bfs
    # use bits to represent lights
    wanted_state = tuple(machine.counters)
    initial_state = tuple([0] * len(wanted_state))

    def visit_state(state, total_presses: int, button: int):
        if button >= len(machine.wirings):
            return total_presses if wanted_state == state else None

        wiring = machine.wirings[button]

        state = list(state)
        is_state_possible = True
        presses = 0
        def press_button():
            nonlocal presses, is_state_possible
            for wire in wiring:
                state[wire] += 1
                if state[wire] > wanted_state[wire]:
                    is_state_possible = False
                    return
            presses += 1

        # press current button as many times a possible
        best_result = None
        while is_state_possible:
            result = visit_state(tuple(state), total_presses+presses, button+1)
            if result is not None and (best_result is None or result < best_result):
                best_result = result
            press_button()

        return best_result
    
    return visit_state(initial_state, 0, 0)

result = 0
for machine in input:
    machine_result = solve(machine)
    print(machine)
    print(machine_result)
    result += machine_result
print(result)