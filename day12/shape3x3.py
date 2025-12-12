"""
represent 3x3 shapes as 9-bit integers
"""

from typing import *

def shape_from_grid(grid: List[List[bool]]) -> int:
    value = 0
    for y in range(3):
        for x in range(3):
            if grid[y][x]:
                value |= 1 << (y * 3 + x)
    return value


def shape_gen_variants(shape: int) -> Set[int]:
    transforms = set()
    for _ in range(2):
        for _ in range(4):
            transforms.add(shape)
            shape = shape_rotate(shape)
        shape = shape_flip(shape)

    return transforms


def shape_get(shape: int, x: int, y: int) -> bool:
    return (shape >> (y * 3 + x)) & 1 != 0


def shape_rotate(shape: int) -> int:
    new_shape = 0
    for y in range(3):
        for x in range(3):
            if shape_get(shape, x, y):
                new_x, new_y = 2 - y, x
                new_shape |= 1 << (new_y * 3 + new_x)
    return new_shape


def shape_flip(shape: int) -> int:
    new_shape = 0
    for y in range(3):
        for x in range(3):
            if shape_get(shape, x, y):
                new_x, new_y = 2 - x, y
                new_shape |= 1 << (y * 3 + (2 - x))
    return new_shape


def shape_str(shape: int, indent: str = "") -> str:
    lines = []
    for y in range(3):
        line = "".join("#" if shape_get(shape, x, y) else "." for x in range(3))
        lines.append(indent + line)
    return "\n".join(lines)


if __name__ == "__main__":
    grids = [
        [[True, True, True], [True, False, True], [True, True, True]],
        [[False, True, True], [True, False, False], [False, True, True]],
        [[False, True, True], [True, False, False], [True, True, True]],
    ]

    for grid in grids:
        shape = shape_from_grid(grid)
        print("\nOriginal shape:")
        print(shape_str(shape))

        print("\nAll variants:")
        for shape in shape_gen_variants(shape):
            print()
            print(shape_str(shape))
