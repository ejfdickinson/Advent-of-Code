def parse_map(data):
    for y,line in enumerate(data.splitlines()):
        for x,s in enumerate([*line]):
            if s == '#':
                yield (x,y)

def expand(galaxies, mul=2):
    xvals, yvals = zip(*galaxies)
    xmax = max(xvals)
    ymax = max(yvals)

    xgaps = [x for x in range(xmax) if x not in xvals]
    ygaps = [y for y in range(ymax) if y not in yvals]

    galaxies_expanded = [
        (
            x + (mul-1) * len([xgap for xgap in xgaps if xgap < x]),
            y + (mul-1) * len([ygap for ygap in ygaps if ygap < y])
        ) for x,y in galaxies
    ]

    return galaxies_expanded

def get_distances(galaxies):    
    distances = {}
    for i,galaxy1 in enumerate(galaxies):
        for k,galaxy2 in enumerate(galaxies[i:]):
            distances[(i,i+k)] = manhattan(*galaxy1, *galaxy2)

    return distances


def manhattan(x1,y1,x2,y2):
    return int(abs(x2-x1) + abs(y2-y1))

def run(data):
    galaxies = list(parse_map(data))
    galaxies_expanded = [
        expand(galaxies, mul=mul) for mul in [1,1e6]
    ]

    distances = [get_distances(galaxies) for galaxies in galaxies_expanded]

    return (
        sum(distances[0].values()),
        sum(distances[1].values())
    )

# Running script
fp = "2023/inputs/day11"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
