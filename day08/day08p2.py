import os

class Point:
    def __init__(self, s: str):
        self.x,self.y,self.z = [int(n) for n in s.split(",")]

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"
    
    def distance(self, other: Point) -> int:
        dx = self.x-other.x
        dy = self.y-other.y
        dz = self.z-other.z
        return dx*dx+dy*dy+dz*dz

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [Point(line) for line in file]

n = len(input)
pairs = []
for i in range(n):
    for j in range(i+1, n):
        a = input[i]
        b = input[j]
        distance = a.distance(b)
        pairs.append((distance, i, j))

pairs.sort()

circuits = dict()
circuit_by_box = dict()

def connect(i, j):
    if i in circuit_by_box:
        ci = circuit_by_box[i]
    else:
        circuit_by_box[i] = i
        circuits[i] = set([i])
        ci = i

    if j in circuit_by_box:
        cj = circuit_by_box[j]
    else:
        circuit_by_box[j] = j
        circuits[j] = set([j])
        cj = j

    if ci == cj:
        return

    circuits[ci] = circuits[ci].union(circuits[cj])
    for j in circuits[cj]:
        circuit_by_box[j] = ci
    del circuits[cj]
    

for distance, i, j in pairs:
    connect(i, j)
    if len(circuits) == 1 and len(circuits[circuit_by_box[i]]) == len(input):
        print(input[i], input[j])
        print(input[i].x * input[j].x)
        break