import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [range_str.split("-") for range_str in file.read().split(",")]

"""
for every range we want to find all numbers that are formed from repetition of the digits, like 123123, where 123 is repeated
we are only interested in numbers of even length
we can interate over all possible numbers that are repeated twice, 123 in this example

for each length the upper and lower bound is either the shortest number of this length 100 or longest number of this length 999
or maximum/minimum of the lower/higher badge upper/lower half

"""

total = 0
for start_str, end_str in input:
    start = int(start_str)
    end = int(end_str)
    subtotal = 0
    
    for l in range(len(start_str), len(end_str) + 1):
        if l % 2 != 0:
            continue

        if l == len(start_str):
            lower = int(start_str[: l // 2])
        else:
            lower = int("1" + "0" * (l // 2 - 1))

        if l == len(end_str):
            higher = int(end_str[: l // 2])
        else:
            higher = int("9" * (l // 2))

        pow10 = int("1" + "0" * (l // 2))

        for num in range(lower, higher + 1):
            numnum = num + num * pow10
            if start <= numnum <= end:
                subtotal += numnum
    total += subtotal

print(total)
