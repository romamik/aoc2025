import input
from shape3x3 import *
from typing import *

names = (
    [chr(i) for i in range(ord("a"), ord("z") + 1)]
    + [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    + [chr(i) for i in range(ord("0"), ord("9") + 1)]
)

def solve(
    width: int, height: int, shapes: Dict[int, List[int]], shape_counts: List[int]
) -> bool:
    grid = [["."] * width for _ in range(height)]
    placed_count = 0

    def can_place(shape: int, x: int, y: int) -> bool:
        for yy in range(0, 3):
            for xx in range(0, 3):
                if shape_get(shape, xx, yy) and grid[y + yy][x + xx] != ".":
                    return False

        if placed_count == 0:
            return True

        # only allow if there is something in the neighborhood
        for yy in range(max(0, y - 1), min(height, y + 4)):
            for xx in range(max(0, x - 1), min(width, x + 4)):
                if grid[yy][xx] != ".":
                    return True

        return False

    def place(shape: int, x: int, y: int, val: str):
        nonlocal placed_count

        if val == ".":
            placed_count -= 1
        else:
            placed_count += 1

        for yy in range(0, 3):
            for xx in range(0, 3):
                if shape_get(shape, xx, yy):
                    grid[y + yy][x + xx] = val

    def grid_key() -> str:
        return "".join("".join("." if c == "." else "#" for c in line) for line in grid)

    def print_grid():
        for line in grid:
            print("".join(line))

    unplaced = []
    need_cells = 0
    for shape_id, count in enumerate(shape_counts):
        shape0 = next(iter(shapes[shape_id]))
        for y in range(0, 3):
            for x in range(0, 3):
                if shape_get(shape0, x, y):
                    need_cells += count
        for _ in range(count):
            name = names[len(unplaced) % len(names)]
            unplaced.append((name, shapes[shape_id]))
    
    if need_cells > width * height:
        return False

    visited = set()

    def search() -> bool:
        if len(unplaced) == 0:
            return True

        key = grid_key()
        if key in visited:
            return False
        visited.add(key)

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
    shapes, rects = input.read_input("input.txt")

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
