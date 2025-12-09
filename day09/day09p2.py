import os
from typing import *


class Point:
    def __init__(self, s: str):
        self.x, self.y = [int(p) for p in s.split(",")]

    def __repr__(self) -> str:
        return f"Pt({self.x}, {self.y})"

    def __eq__(self, value) -> bool:
        return self.x == value.x and self.y == value.y


with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [Point(line) for line in file if len(line.strip()) > 0]

all_x = list(set(pt.x for pt in input))
all_y = list(set(pt.y for pt in input))
all_x.sort()
all_y.sort()

# we want to "compress space"
# we create a grid with all unique x and y
# we are interested in the state of cells in such grid: are they filled or not
#
# actually we can create a grid where there are cells for exact x or y or spaces between them
# let's call indices in this grid xx and yy

"""
gets sorted list of coordinates
creates a mapping from normal coordinates to compressed coordinates

in compressed space adjacent points have distance 
    * 0 - if they have distance ==0 in normal coordinates
    * 1 - if they have distance > 0 in normal coordinates

[1,2,10,11,15] will be compressed to
[0,1,3,4,6]
and mappings will be [1:0, 1:2, 10:3, 11:4, 15:6]
"""


def compress_axis(all_t: List[int]) -> Dict[int, int]:
    tt_by_t: Dict[int, int] = {}
    tt_by_t[all_t[0]] = 0
    tt = 1
    for i in range(1, len(all_t)):
        prev_t = all_t[i - 1]
        t = all_t[i]
        if prev_t < t - 1:
            tt += 1
        tt_by_t[t] = tt
        tt += 1
    return tt_by_t


xx_by_x = compress_axis(all_x)
yy_by_y = compress_axis(all_y)
width = xx_by_x[all_x[-1]] + 1
height = yy_by_y[all_y[-1]] + 1

canvas = [[0] * width for _ in range(height)]

# draw lines
# we only draw vertical lines and we write -1 or 1 depending on direction up or down
for i in range(len(input)):
    prev_pt = input[i]
    pt = input[(i + 1) % len(input)]
    if prev_pt.x == pt.x:
        xx = xx_by_x[pt.x]
        yy0 = yy_by_y[prev_pt.y]
        yy1 = yy_by_y[pt.y]
        dyy = 1 if yy1 > yy0 else -1
        for yy in range(yy0, yy1 + dyy, dyy):
            canvas[yy][xx] = dyy

# fill
for yy in range(height):
    inside = 0
    for xx in range(width):
        v = canvas[yy][xx]
        if inside != v:
            inside += v
        if inside != 0 or v != 0:
            canvas[yy][xx] = 1

# # print canvas
# for yy in range(height):
#     s = ""
#     for xx in range(width):
#         s += str(canvas[yy][xx])
#     print(s)


def is_filled(x0, x1, y0, y1) -> bool:
    xx0 = xx_by_x[x0]
    xx1 = xx_by_x[x1]
    yy0 = yy_by_y[y0]
    yy1 = yy_by_y[y1]
    for xx in range(xx0, xx1 + 1):
        for yy in range(yy0, yy1 + 1):
            if canvas[yy][xx] == 0:
                return False
    return True

max_area = 0
for i, a in enumerate(input):
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
