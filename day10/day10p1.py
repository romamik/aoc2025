import os
from collections import deque

class MachineDescr:
    def __init__(self, s: str):
        i = s.index("]")
        self.lights = [c == '#' for c in s[1:i]]

        j = s.index("{")
        self.wirings = [[int(strnum) for strnum in parens[1:-1].split(",")] for parens in s[i+1:j].split()]

    def __repr__(self):
        return f"(lights:{self.lights} wiring:{self.wirings})"


with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [MachineDescr(line) for line in file]

# initially the lights are off
# pressing a button toggles the lights in wiring
# we want to get lights to match the given confiuration

def solve(machine: MachineDescr) -> int:
    # do the bfs
    # use bits to represent lights
    wanted_state = 0
    for bit, bit_value in enumerate(machine.lights):
        if bit_value:
            wanted_state |= (1<<bit)

    # convert button wirings to bits so we can do xor to toggle bits
    wirings = []
    for wiring in machine.wirings:
        w = 0
        for bit in wiring:
            w |= (1 <<bit)
        wirings.append(w)

    queue = deque([0])
    visited = {0:0}
    while len(queue)>0:
        state = queue.popleft()
        presses = visited[state]
        for wiring in wirings:
            next_state = state ^ wiring
            next_presses = presses+1
            if next_state == wanted_state:
                return next_presses

            if next_state not in visited:
                visited[next_state] = next_presses
                queue.append(next_state)

    return -1

result = 0
for machine in input:
    result += solve(machine)
print(result)