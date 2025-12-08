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

"""
when we connect two boxes, we make one parent of the other
this can form a tree
the root of the tree identifies the circuit
"""
parents = {}
size = {}
def get_circuit(i: int) -> int:
    if i not in parents:
        parents[i] = i
        size[i] = 1
        return i
    p = parents[i]
    if p != i:
        p = get_circuit(p)
        parents[i] = p
    return p

def connect(i: int, j: int):
    i = get_circuit(i)
    j = get_circuit(j)
    parents[i] = j
    size[j] += size[i]

for distance, i, j in pairs:
    ci = get_circuit(i)
    cj = get_circuit(j)
    if ci != cj:
        connect(i, j)
        # print(f"connect {i} {j}")
        ci = get_circuit(i)
        # print(ci, [t for t in parents if get_circuit(t) == ci])
        if size[ci] == len(input):
            print(input[i], input[j])
            print(input[i].x*input[j].x)
            break
