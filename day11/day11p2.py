import os
from typing import *
from collections import *

with open(os.path.dirname(__file__) + "/input.txt", "r") as file:
    connections: defaultdict[str, List[str]] = defaultdict(list)
    for line in file:
        device, output = line.split(":")
        output = output.strip().split()
        connections[device] = output

"""
In part 1 I used BFS to just count all possible paths. I could have used DFS the same way.
But this process actually explores all possible paths and that can be time consuming as there can be a lot of paths.

Instead for each node we can count paths that lead to it. And only then expand to next nodes. 
To do this before visiting a node we should visit all nodes that lead to it from the source.

We can sort graph in topological order and then process node one by one.
In topological order we can be sure that all previous nodes were visited, so we can just look at incoming connections and sum up.

We need to count paths from 'svr' to 'out' that visit 'fft' and 'dac' in any order
We can separately count paths from 'svr' to 'fft', from 'fft' to 'dac', and from 'dac' to 'out'
and also 'svr' to 'dac', 'dac' to 'fft' and 'fft' to out

"""

# find incoming connections, or reverse graph
def calc_incoming(connections: Dict[str, List[str]]) -> defaultdict[str, List[str]]:
    incoming: defaultdict[str, List[str]] = defaultdict(list)
    for device, output in connections.items():
        for out_device in output:
            if out_device not in incoming:
                incoming[out_device] = [device]
            else:
                incoming[out_device].append(device)
    return incoming


# topological sort
# start with nodes without incoming connections
# remove them from graph,
# proceed with nodes that lost all incoming connections
def toposort(
    connections: Dict[str, List[str]], incoming: Dict[str, List[str]]
) -> List[str]:
    # count incoming connections
    incoming_count = {device: len(incoming) for device, incoming in incoming.items()}

    topo_order = []

    q = [
        device
        for device in connections
        if device not in incoming_count or incoming_count[device] == 0
    ]
    while len(q) > 0:
        device = q.pop()
        topo_order.append(device)
        for out_device in connections[device]:
            incoming_count[out_device] -= 1
            if incoming_count[out_device] == 0:
                q.append(out_device)

    return topo_order


def count_paths(
    start: str, end: str, topo_order: List[str], incoming: Dict[str, List[str]]
) -> int:
    path_counts: defaultdict[str, int] = defaultdict(int)
    start_idx = topo_order.index(start)
    end_idx = topo_order.index(end)
    path_counts[start] = 1
    for device in topo_order[start_idx + 1 : end_idx + 1]:
        path_counts[device] = sum(
            path_counts[in_device] for in_device in incoming[device]
        )
    return path_counts[end]


incoming = calc_incoming(connections)
topo_order = toposort(connections, incoming)

svr2fft = count_paths("svr", "fft", topo_order, incoming)
fft2dac = count_paths("fft", "dac", topo_order, incoming)
dac2out = count_paths("dac", "out", topo_order, incoming)
svr2dac = count_paths("svr", "dac", topo_order, incoming)
dac2fft = count_paths("dac", "fft", topo_order, incoming)
fft2out = count_paths("fft", "out", topo_order, incoming)

print(svr2fft*fft2dac*dac2out + svr2dac* dac2fft* fft2out)