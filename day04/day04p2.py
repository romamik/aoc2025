import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [list(line) for line in (line.strip() for line in file) if len(line) > 0]

rows, cols = len(input), len(input[0])

def neighbors(row, col):
    for nei_r in range(row - 1, row + 2):
        for nei_c in range(col - 1, col + 2):
            if nei_r == row and nei_c == col:
                continue
            if not (0 <= nei_r < rows and 0 <= nei_c < cols):
                continue
            yield nei_r, nei_c
    

nei_counts = [[0]*cols for _ in range(rows)]
can_remove = []
for row in range(rows):
    for col in range(cols):
        if input[row][col] == ".":
            continue
        nei_count = 0
        for nei_r, nei_c in neighbors(row, col):
            if input[nei_r][nei_c] != ".":
                nei_count += 1
        nei_counts[row][col] = nei_count
        if nei_count < 4:
            can_remove.append((row, col))
            input[row][col] = "_"

removed_count = 0
while can_remove:
    row, col = can_remove.pop()
    removed_count += 1
    for nei_r, nei_c in neighbors(row, col):
        if input[nei_r][nei_c] != "@":
            continue
        nei_counts[nei_r][nei_c] -= 1
        if nei_counts[nei_r][nei_c] < 4:
            can_remove.append((nei_r, nei_c))
            input[nei_r][nei_c] = "_"

print(removed_count)
