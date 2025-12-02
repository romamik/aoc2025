import os

with open(os.path.dirname(__file__) + '/input.txt', 'r') as file:
    rotations = [(1 if line[0] == 'R' else -1, int(line[1:])) for line in file]

pos = 50
count = 0
for dir, rotation in rotations:
    pos = (pos + dir*(rotation % 100) + 100) % 100
    if pos == 0:
        count += 1
print(count)