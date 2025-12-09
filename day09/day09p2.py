import os
from copy import copy


class Point:
    def __init__(self, s: str):
        self.x, self.y = [int(p) for p in s.split(",")]

    def __repr__(self) -> str:
        return f"Pt({self.x}, {self.y})"

    def __eq__(self, value) -> bool:
        return self.x == value.x and self.y == value.y


with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [Point(line) for line in file if len(line.strip()) > 0]

max_x = max(pt.x for pt in input)
max_y = max(pt.y for pt in input)
min_x = min(pt.x for pt in input)
min_y = min(pt.y for pt in input)
width = max_x - min_x + 1
height = max_y - min_y + 1
print(min_x, min_y, max_x, max_y)

canvas = [0] * (width * height)


def set_at(x, y, v):
    canvas[(x - min_x) + (y - min_y) * width] = v


def get_at(x, y):
    return canvas[(x - min_x) + (y - min_y) * width]


# draw lines
for i in range(len(input)):
    prev_pt = input[i]
    pt = input[(i + 1) % len(input)]
    if prev_pt.x == pt.x:
        x = pt.x
        y0 = prev_pt.y
        y1 = pt.y
        dy = 1 if y1 > y0 else -1
        for y in range(y0, y1 + dy, dy):
            set_at(x, y, dy)

# fill
for y in range(min_y, max_y + 1):
    print(f"fill {y-min_y}/{height}")
    inside = 0
    for x in range(min_x, max_x + 1):
        v = get_at(x, y)
        if inside != v:
            inside += v
        set_at(x, y, "." if inside == 0 else "#")

# print canvas
# for y in range(min_y, max_y + 1):
#     s = ""
#     for x in range(min_x, max_x + 1):
#         s += str(get_at(x, y))
#     print(s)

def is_filled(x0, x1, y0, y1) -> bool:
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            if get_at(x, y) != "#":
                return False
    return True

max_area = 0
for i, a in enumerate(input):
    print(f"search {i}/{len(input)}")
    for j in range(i + 1, len(input)):
        b = input[j]
        dx = abs(a.x - b.x) + 1
        dy = abs(a.y - b.y) + 1
        area = dx * dy
        if area > max_area:
            x0, x1 = min(a.x,b.x), max(a.x, b.x)
            y0, y1= min(a.y,b.y), max(a.y, b.y)
            if is_filled(x0, x1, y0, y1):
                max_area = area
print(max_area)