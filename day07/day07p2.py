import os

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [list(line) for line in file]

particles = [0] * len(input[0])

for i in range(1, len(input)):
    prev_line = input[i - 1]
    line = input[i]
    for j in range(len(line)):
        prev = prev_line[j]
        char = line[j]
        if prev == "S":
            particles[j] = 1
        if particles[j] > 0 and char == "^":
            particles[j - 1] += particles[j]
            particles[j + 1] += particles[j]
            particles[j] = 0
            
print(sum(particles))
