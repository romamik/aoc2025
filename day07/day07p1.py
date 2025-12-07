import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [list(line) for line in file]

split_count = 0

for i in range(1, len(input)):
    prev_line = input[i - 1]
    line = input[i]
    for j in range(len(line)):
        prev = prev_line[j]
        char = line[j]
        if prev == "S":
            if line[j] != ".":
                raise Exception("expected . under S")
            line[j] = "|"
        if prev == "|":
            match char:
                case ".":
                    line[j] = "|"
                case "^":
                    split_count += 1
                    assert line[j - 1] in "|."
                    assert line[j + 1] in "|."
                    line[j - 1] = "|"
                    line[j + 1] = "|"
                case "|":
                    pass
                case _:
                    raise Exception(f"unexpected char {char}")

print(split_count)
