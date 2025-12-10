import os
from collections import defaultdict

class MachineDescr:
    def __init__(self, s: str):
        s = s.strip()
        i = s.index("]")
        self.lights = [c == '#' for c in s[1:i]]

        j = s.index("{")
        self.buttons = [[int(strnum) for strnum in parens[1:-1].split(",")] for parens in s[i+1:j].split()]

        self.counters = [int(strnum) for strnum in s[j+1:-1].split(",")]

    def __repr__(self):
        return f"(lights:{self.lights} buttons:{self.buttons} counters:{self.counters})"


with open(os.path.dirname(__file__) + "/test2.txt", "r") as file:
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
#
# for each counter we know which buttons are wired to it
# sum of presses to these buttons should equal to final counter value
# this gives are a set of equations
# 
# for this machine 0:(3) 1:(1,3) 2:(2) 3:(2,3) 4:(0,2) 5:(0,1) {3,5,4,7}
# it will be
# counter 0 == 3, wired to buttons 4:(0,2) and 5:(0,1)   -- 3 == p4+p5
# counter 1 == 5, wired to buttons 1 and 5               -- 5 == p1+p5
# counter 2 == 4, wired to buttons 2, 3 and 4            -- 4 == p2+p3+p4
# counter 3 == 7, wired to buttons 0, 1 and 3            -- 7 == p0+p1+p3
# 
# when trying presses we can try to calculate numbers of presses for other buttons if possible
# for example if we already decided with p0 and p1 we know the value for p3, if we know p3 and p3 we know the value for p4
# this can reduce the number of variants significantly
#
# but this seems complicated to implement
#
# each press of the button increments total sum by number of counters it affects
# we want to reach final state (and final sum) as fast as possible
# we should prefer to press buttons connected to maximum number of counters for that as much as possible


def solve(machine: MachineDescr) -> int:
    wanted_state = tuple(machine.counters)
    state = [0] * len(wanted_state)
    btn_presses = [0] * len(machine.buttons)
    total_presses = 0

    buttons = list(machine.buttons)
    buttons.sort(key=lambda btn: len(btn), reverse=True)

    def press_button(button: int, count: int):
        nonlocal total_presses
        wiring = buttons[button]
        for wire in wiring:
            state[wire] += count
        btn_presses[button] += count
        total_presses += count

    def is_state_good() -> bool:
        for i, wanted in enumerate(wanted_state):
            if state[i] > wanted:
                return False
        return True
    
    # print("buttons", buttons)
    # print("wanted_state", wanted_state)
    
    def visit_state(button: int) -> int | None:
        # print("state", state, "presses", btn_presses)
        if button >= len(buttons):
            return total_presses if wanted_state == tuple(state) else None

        # press current button as many times a possible
        while is_state_good():
            press_button(button, 1)
        
        # decrement number of presses to zero
        while btn_presses[button] > 0:
            press_button(button, -1)
            result = visit_state(button+1)
            if result is not None:
                return result

        return None
    
    return visit_state(0)

result = 0
for machine in input:
    machine_result = solve(machine)
    print(machine)
    print(machine_result)
    result += machine_result
print(result)