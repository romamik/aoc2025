import os
from typing import *
from collections import *

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    connections: Dict[str, List[str]] = {}
    for line in file:
        device, output = line.split(":")
        output = output.strip().split()
        connections[device] = output

queue = deque(["you"])
path_count = Counter()
while len(queue) > 0:
    device = queue.popleft()
    path_count[device] += 1
    if device not in connections:
        continue
    for next in connections[device]:
        queue.append(next)

print(path_count["out"])
