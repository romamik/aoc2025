import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [
        tuple(int(strnum) for strnum in line.split(","))
        for line in file
        if len(line.strip()) > 0
    ]

n = len(input)
max_area = 0
for i, a in enumerate(input):
    for j in range(i + 1, n):
        b = input[j]
        dx = abs(a[0] - b[0]) + 1
        dy = abs(a[1] - b[1]) + 1
        area = dx * dy
        max_area = max(max_area, area)
print(max_area)
