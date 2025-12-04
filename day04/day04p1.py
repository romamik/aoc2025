import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [list(line) for line in (line.strip() for line in file) if len(line) > 0]

rows, cols = len(input), len(input[0])

accessible_rolls = 0
for row in range(rows):
    for col in range(cols):
        neighbors = 0
        if input[row][col] != "@":
            continue
        for nei_r in range(row - 1, row + 2):
            for nei_c in range(col - 1, col + 2):
                if nei_r == row and nei_c == col:
                    continue
                if not (0 <= nei_r < rows and 0 <= nei_c < cols):
                    continue
                if input[nei_r][nei_c] != ".":
                    neighbors += 1
        if neighbors < 4:
            accessible_rolls += 1

print(accessible_rolls)
