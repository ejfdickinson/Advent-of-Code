# Rough brute-force method, will not work for Part 2!

def parse_rocks(data):
    lines = data.splitlines()
    ymax = len(lines)
    xmax = len(lines[0])

    rolling = []
    fixed = []

    for j,line in enumerate(lines):
        y = ymax - j
        for i,s in enumerate([*line]):
            x = i+1
            if s == 'O':
                rolling.append((x,y))
            if s == '#':
                fixed.append((x,y))

    return rolling, fixed, xmax, ymax

def run_cycle(rolling, fixed, xmax, ymax):
    tilted =  tilt(rolling, fixed, xmax, ymax, direction='N')
    tilted =  tilt(tilted, fixed, xmax, ymax, direction='W')
    tilted =  tilt(tilted, fixed, xmax, ymax, direction='S')
    tilted =  tilt(tilted, fixed, xmax, ymax, direction='E')

    return tilted

def tilt(rolling, fixed, xmax, ymax, direction='N'):
    if direction == 'N':
        xdisp,ydisp = (0,1)
    elif direction == 'S':
        xdisp,ydisp = (0,-1)
    elif direction == 'E':
        xdisp,ydisp = (1,0)
    elif direction == 'W':
        xdisp,ydisp = (-1,0)
    else:
        raise ValueError("Unsupported tilt direction!")
    
    tilted = rolling.copy()

    # For tilt north/south, proceed by col then by row
    if direction == 'N' or direction == 'S':
        for x in range(1,xmax+1):
            rocks_to_roll = sorted([(xrock,yrock) for xrock,yrock in tilted if xrock == x], reverse=(direction == 'N'))

            for xrock,yrock in rocks_to_roll:
                xrock_new = xrock
                yrock_new = yrock
                while not is_blocked(xrock_new + xdisp,yrock_new + ydisp, tilted, fixed, xmax, ymax):
                    xrock_new += xdisp
                    yrock_new += ydisp

                tilted.remove((xrock,yrock))
                tilted.append((xrock_new,yrock_new))
    else:
        # For tilt east/west, proceed by row then by col
        for y in range(1,ymax+1):
            rocks_to_roll = sorted([(xrock,yrock) for xrock,yrock in tilted if yrock == y], reverse=(direction == 'E'))

            for xrock,yrock in rocks_to_roll:
                xrock_new = xrock
                yrock_new = yrock
                while not is_blocked(xrock_new + xdisp,yrock_new + ydisp, tilted, fixed, xmax, ymax):
                    xrock_new += xdisp
                    yrock_new += ydisp

                tilted.remove((xrock,yrock))
                tilted.append((xrock_new,yrock_new))

    return tilted

def is_blocked(x, y, rolling, fixed, xmax, ymax):
    if x < 0 or x > xmax:
        return True
    
    if y < 0 or y > ymax:
        return True
    
    if (x,y) in rolling or (x,y) in fixed:
        return True
    
    return False

def compute_load(rocks):
    return sum(
        [y for _,y in rocks]
    )

def run(data):
    rolling, fixed, xmax, ymax = parse_rocks(data)
    
    tilted_north = sorted(tilt(rolling, fixed, xmax, ymax, direction='N'))

    n_cycles = 1e9
    for i in range(int(n_cycles)):
        rolling_new = run_cycle(rolling, fixed, xmax, ymax)
        
        if rolling_new == rolling:
            break
        else:
            rolling = rolling_new

    return (
        compute_load(tilted_north),
    )

# Running script
fp = "2023/inputs/day14"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
