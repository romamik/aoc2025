import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [line.split() for line in file]

num_problems = len(input[0])
num_operands = len(input)-1
total = 0
for problem in range(num_problems):
    operator = input[num_operands][problem]
    result = 0
    if operator == '+': result = 0
    elif operator == '*': result = 1
    else: raise Exception(f"Unknown operator {operator}")
    print(operator)
    for operand in range(num_operands):
        num = int(input[operand][problem])
        print(num)
        match operator:
            case '+': result += num
            case '*': result *= num
            case _: raise Exception(f"Unknown operator {operator}")
    print(f"={result}")
    total += result

print(total)

