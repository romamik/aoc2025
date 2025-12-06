import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [line for line in file]

# we can use last line of input (with operators) to separate problems
# when we encounter the operator it starts the new problem

i = 0
total = 0

while i < len(input[-1]):
    op = input[-1][i]

    match op:
        case '+': result = 0
        case '*': result = 1
        case _: raise Exception(f"unknown op '{op}'")

    print(op)
    
    while True:
        num = 0
        for j in range(len(input)-1):
            if '0' <= input[j][i] <= '9':
                num = num * 10 + int(input[j][i])
        if num != 0:                
            print(num)
            match op:
                case '+': result += num
                case '*': result *= num
                case _: raise Exception(f"unknown op '{op}'")
        
        i += 1
        if i >= len(input[-1]) or input[-1][i] != ' ':
            break

    print(f"={result}")
    total += result

print(total)
    