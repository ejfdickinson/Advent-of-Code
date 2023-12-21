# Improved method for single garden

def parse_map(data):
    start = None
    blocked = []

    lines = data.splitlines()
    size = (len(lines[0]), len(lines))

    for y,line in enumerate(lines):
        for x,c in enumerate([*line]):
            if c == "S":
                start = (x,y)
            elif c == '#':
                blocked.append((x,y))

    return start, blocked, size

def in_bounds(new_plot, size):
    x,y = new_plot
    xmax, ymax = size

    return (
        x >= 0 and
        y >= 0 and
        x < xmax and
        y < ymax
    )

def get_neighbors(plot):
    CARDINAL = [(-1,0), (1,0), (0,-1), (0,1)]
    x,y = plot
    return [
        (x+dx, y+dy) for dx,dy in CARDINAL
    ]

def accessible(size, blocked, start, n_steps):
    # Any plot that is accessible in n_steps is also accessible in n_steps + 2 * i, for i = 0,1,2,3 ...
    # Find n_steps_min for each plot. Check that the plot is accessible via the shortest path. If so, include if same even/odd as n_steps.

    path = shortest_path(size, blocked, start)

    plots = [
        k for k,v in path.items()
        if v <= n_steps and (v % 2) == (n_steps % 2)
    ]

    return plots

def shortest_path(size, blocked, start):
    # Simple Dijkstra

    path = {}
    count = 0
    neighbors = [start]

    while len(neighbors) > 0:
        for plot in neighbors:
            path[plot] = count
        
        count += 1
        new_neighbors = []
        for plot in neighbors.copy():
            new_neighbors.extend([
                new for new in get_neighbors(plot)
                if (new not in blocked) and (new not in path) and in_bounds(new, size)
            ])
        
        neighbors = set(new_neighbors)

    return path

def run(data):
    start, blocked, size = parse_map(data)

    # n_steps = 6
    n_steps = 64
    plots = accessible(size, blocked, start, n_steps)

    return (
        len(plots)
    )

# Running script
fp = "2023/inputs/day21"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
