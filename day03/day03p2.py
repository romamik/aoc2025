import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [line for line in (line.strip() for line in file) if len(line) > 0]

num_sum = 0
for line in input:
    remain_line = line
    num_str = ""
    while len(num_str) < 12:
        min_len_after = 11 - len(num_str)
        max_char = ""
        max_i = -1
        for i in range(len(remain_line) - min_len_after):
            if remain_line[i] > max_char:
                max_char = remain_line[i]
                max_i = i
        
        num_str += max_char
        remain_line = remain_line[max_i+1:]

    num = int(num_str)
    # print(line, num)
    num_sum+=num

print(num_sum)
