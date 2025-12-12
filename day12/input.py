import os
from typing import *

type Shapes = Dict[int, List[List[bool]]]
type Rects = List[Tuple[int, int, List[int]]]

def read_input(fname: str) -> Tuple[Shapes, Rects]:
    file = open(f"{os.path.dirname(__file__)}/{fname}", "r") 
    
    shapes: Shapes = {}
    rects: Rects = []
    while True:
        # parse header
        line = next(file, None)
        if line is None:
            break
        line = line.strip().split(":")
        if len(line[1]) == 0:
            shape_id = int(line[0])
            shape = [[c=="#" for c in next(file).strip()] for _ in range(3)]
            shapes[shape_id] = shape
            next(file)
        elif len(line) == 2:
            width, height = tuple(int(s) for s in line[0].split("x"))
            shape_counts = [int(s) for s in line[1].strip().split()]
            rects.append((width, height, shape_counts))

    return shapes, rects


