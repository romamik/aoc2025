import os
import bisect

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    input = [part.split("\n") for part in file.read().split("\n\n")]
    ranges = [tuple([int(s) for s in line.split("-")]) for line in input[0]]
    ids = [int(s) for s in input[1]]

ranges.sort()
start0, end0 = ranges[0]

# normalized ranges
# [start, end, start, end]
# end is the start of the range where products are spoiled
# so at even indices start ranges with fresh products and at odd indices start ranges with spoiled products
# no intersections
ranges2 = [start0]
cur_end = end0
for start, end in ranges[1:]:
    if start > cur_end+1:
        ranges2.append(cur_end+1)
        ranges2.append(start)
        cur_end = end
    if end > cur_end:
        cur_end = end
ranges2.append(cur_end+1)

# print(ranges)
# print(ranges2)

num_fresh = 0
for id in ids:
    # bisect_right finds position of the last insertion point, or the first element with value > id
    # or in our case the index of the element that starts the next range in ranges2
    # so if index is odd, id falls into even range and that means product is fresh and vice versa
    index = bisect.bisect_right(ranges2, id)
    if index % 2 == 1:
        num_fresh += 1
    # print(id, index % 2 == 0)

print("num_fresh: ", num_fresh)

total_fresh = 0
for i in range(0, len(ranges2), 2):
    start, end = ranges2[i], ranges2[i+1]
    total_fresh += end - start
print("total_fresh: ", total_fresh)
