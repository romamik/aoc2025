import os

with open(os.path.dirname(__file__) + '/input.txt', 'r') as file:
    rotations = [(1 if line[0] == 'R' else -1, int(line[1:])) for line in file]

pos = 50
count = 0
for dir, rotation in rotations:
    # for r in range(rotation):
    #     pos = (pos+dir+100)%100
    #     if pos == 0:
    #         count+=1
    next_pos = pos + dir*rotation
    
    # how many times it will point to zero between pos and next_pos?
    # pos // 100 -- how many times it will cross zero going to pos from zero
    count += abs(next_pos // 100 - pos // 100)
    pos = (100+next_pos % 100)%100
    
print(count)

