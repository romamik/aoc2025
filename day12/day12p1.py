import input
from shape3x3 import *
from typing import *


def solve(
    width: int, height: int, shapes: Dict[int, List[int]], shape_counts: List[int]
) -> bool:
    grid = [["."] * width for _ in range(height)]

    def can_place(shape: int, x: int, y: int) -> bool:
        for yy in range(0, 3):
            for xx in range(0, 3):
                if shape_get(shape, xx, yy) and grid[y + yy][x + xx] != ".":
                    return False
        return True

    def place(shape: int, x: int, y: int, val: str):
        for yy in range(0, 3):
            for xx in range(0, 3):
                if shape_get(shape, xx, yy):
                    grid[y + yy][x + xx] = val

    def print_grid():
        for line in grid:
            print("".join(line))

    unplaced = []
    for shape_id, count in enumerate(shape_counts):
        for _ in range(count):
            name = chr(ord("A") + len(unplaced))
            unplaced.append((name, shapes[shape_id]))

    def search() -> bool:
        if len(unplaced) == 0:
            return True

        name, variants = unplaced.pop()

        for y in range(0, height - 3 + 1):
            for x in range(0, width - 3 + 1):
                for variant in variants:
                    if can_place(variant, x, y):
                        place(variant, x, y, name)
                        if search():
                            return True
                        place(variant, x, y, ".")

        unplaced.append((name, variants))
        return False

    if search():
        print_grid()
        return True

    print("impossible")
    return False


def main():
    shapes, rects = input.read_input("test.txt")

    shapes = {
        shape_id: shape_gen_variants(shape_from_grid(grid))
        for shape_id, grid in shapes.items()
    }

    count = 0
    for width, height, shape_counts in rects:
        print()
        print(width, height, shape_counts)
        if solve(width, height, shapes, shape_counts):
            count += 1
    print(count)


if __name__ == "__main__":
    main()
