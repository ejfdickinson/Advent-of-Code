# Naive brute-force does not work for Day 8b

# Identify repeating cycles for each start node and find LCD?

import re

def parse_nodes(data):
    nodes = {}
    for line in data.splitlines():
        names = re.findall(r'(\w+)', line)
        nodes[names[0]] = {
            "L": names[1],
            "R": names[2]
        }

    return nodes

def count_steps(network, path, start="AAA", end="ZZZ"):
    currnode = start
    pathlen = len(path)

    steps = 0
    pathstep = 0
    while currnode != end:
        currnode = network[currnode][path[pathstep]]
        steps += 1
        pathstep += 1
        if pathstep == pathlen:
            pathstep = 0

    return steps

def count_steps_ghostlike(network, path, start="A", end="Z"):
    currnodes = [node for node in network if node[-1] == start]
    pathlen = len(path)

    steps = 0
    pathstep = 0
    while any([node[-1] != end for node in currnodes]):
        currnodes = [network[currnode][path[pathstep]] for currnode in currnodes.copy()]
        steps += 1
        pathstep += 1
        if pathstep == pathlen:
            pathstep = 0

    return steps

def run(data):
    path, node_info = data.split("\n\n")
    network = parse_nodes(node_info)
    
    steps = count_steps(network, path)
    steps_ghostlike = count_steps_ghostlike(network, path)

    return (
        steps,
        steps_ghostlike
    )

# Running script
fp = "2023/inputs/day8"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
