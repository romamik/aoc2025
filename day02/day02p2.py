import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [range_str.strip().split("-") for range_str in file.read().split(",")]

total = 0
for start_str, end_str in input:
    visited = set()
    start = int(start_str)
    end = int(end_str)
    subtotal = 0
    for l in range(len(start_str), len(end_str) + 1):
        for sub in range(2, l+1):
            if l % sub != 0:
                continue

            if l == len(start_str):
                lower = int(start_str[: l // sub])
            else:
                lower = int("1" + "0" * (l // sub - 1))

            if l == len(end_str):
                higher = int(end_str[: l // sub])
            else:
                higher = int("9" * (l // sub))

            for num in range(lower, higher + 1):
                numnum = int(str(num) * sub)
                if numnum not in visited and start <= numnum <= end:
                    subtotal += numnum
                visited.add(numnum)
    total += subtotal

print(total)
