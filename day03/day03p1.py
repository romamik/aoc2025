import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [line for line in (line.strip() for line in file) if len(line) > 0]

num_sum = 0
for line in input:
    max_char = ""
    max_char2 = ""
    for i, char in enumerate(line):
        if char > max_char and i +1 < len(line):
            max_char = char
            max_char2 = ""
        elif char > max_char2:
            max_char2 = char
    num = int(max_char+max_char2)
    # print(line, num)
    num_sum+=num

print(num_sum)
