# Rough and ready solution to first part only!

from math import ceil

def parse_map(data):
    lines = data.splitlines()
    ymax = len(lines)

    return {
        (i,ymax-j-1): s
        for j,line in enumerate(lines)
        for i,s in enumerate([*line])
    }

def find_distances(pipemap):
    distances = {}
    curr = get_start(pipemap)
    distance = 0
    
    distances[curr] = distance
    closed_loop = False
    while not closed_loop:
        distance += 1
        prev,next = adj(pipemap, curr)
        if prev in distances and next in distances:
            closed_loop = True
        elif prev in distances:
            distances[next] = distance
            curr = next
        else:
            distances[prev] = distance
            curr = prev

    loop_distance = 1 + max(distances.values())

    max_distance = ceil(loop_distance / 2)

    for k,v in distances.items():
        if v > max_distance:
            distances[k] = 2 * max_distance - v

    return distances

def get_start(pipemap):
    for k,v in pipemap.items():
        if v == 'S':
            return k

def adj(pipemap, coord):
    v = pipemap[coord]
    x,y = coord

    if v == '|':
        return [(x,y-1), (x,y+1)]
    elif v == '-':
        return [(x-1,y), (x+1,y)]
    elif v == 'L':
        return [(x,y+1), (x+1,y)]
    elif v == 'J':
        return [(x,y+1), (x-1,y)]
    elif v == '7':
        return [(x-1,y), (x,y-1)]
    elif v == 'F':
        return [(x+1,y), (x,y-1)]
    elif v == 'S':
        for adj_coord in [(x,y-1),(x-1,y),(x+1,y),(x,y+1)]:
            if (
                adj_coord in pipemap and
                coord in adj(pipemap, adj_coord)
            ):
                return [adj_coord,None]
    else:
        return [None,None]

def run(data):
    pipes = parse_map(data)
    distances = find_distances(pipes)

    return (
        max(distances.values()),
    )

# Running script
fp = "2023/inputs/day10"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
