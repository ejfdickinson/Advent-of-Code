from math import prod

def get_coords_adj(coord,bounds,length=1):
    # Get list of surrounding adjacent coordinates to a (length,1) rectangle
    # with origin coord = x,y on a grid with bounds = xmax,ymax
    coords_adj = []

    x,y = coord
    xmax,ymax = bounds

    xend = x + length - 1

    # Cardinal directions
    if y > 0:
        coords_adj += [(x+i,y-1) for i in range(length)]
    if y < ymax:
        coords_adj += [(x+i,y+1) for i in range(length)]
    if x > 0:
        coords_adj.append((x-1,y))
    if xend < xmax:
        coords_adj.append((xend+1,y))

    # Diagonals
    if y > 0:
        if x > 0:
            coords_adj.append((x-1,y-1))
        if xend < xmax:
            coords_adj.append((xend+1,y-1))
    if y < ymax:
        if x > 0:
            coords_adj.append((x-1,y+1))
        if xend < xmax:
            coords_adj.append((xend+1,y+1))

    return coords_adj

def get_array_bounds(charmap):
    # Extent of 2D array "charmap"
    xmax = len(charmap[0])-1
    ymax = len(charmap)-1

    return xmax, ymax

class Star:
    def __init__(self, coord):
        self.coord = coord

    def check_if_gear(self, charmap, parts):
        coords_adj = get_coords_adj(self.coord, get_array_bounds(charmap))
        nums_adj = [(x,y) for x,y in coords_adj if charmap[y][x].isnumeric()]
        partid_adj = []

        for coord in nums_adj:
            x,y = coord
            for k,part in enumerate(parts):
                xpart,ypart = part.start
                xpart_end = xpart + part.length - 1

                if (y == ypart and x >= xpart and x <= xpart_end):
                    partid_adj.append(k)
    
        unique_parts_adj = [parts[k] for k in set(partid_adj)]

        if len(unique_parts_adj) == 2:
            self.is_gear = True
            self.gear_ratio = prod([part.val for part in unique_parts_adj])
        else:
            self.is_gear = False

class Number:
    def __init__(self, s, coord_end):
        self.val = int(s)
        # Calculate digit
        x,y = coord_end
        self.length = len(s)
        self.start = (x+1-self.length, y)

    def is_engine_part(self, charmap):        
        chars_adj = [
            charmap[y][x]
            for x,y in get_coords_adj(self.start, get_array_bounds(charmap), length=self.length)
        ]
        
        return any(c != '.' for c in chars_adj)

def make_charmap(data):
    return [[*line] for line in data.splitlines()]

def parse_schematic_numbers(charmap):
    str_number = ''
    for y,line in enumerate(charmap):
        for x,c in enumerate(line):
            if c.isnumeric():
                str_number += c
            elif len(str_number) > 0:
                # Reached end of number
                yield Number(str_number, (x-1,y))
                str_number = ''
        
        if len(str_number) > 0:
            # End of line
            yield Number(str_number, (len(line)-1,y))
            str_number = ''

def parse_schematic_stars(charmap):
    return [Star((x,y)) for y,line in enumerate(charmap) for x,c in enumerate(line) if c == '*'] 

def run(data):
    # Store schematic as 2D array of chars, and parse for number strings and stars (*)
    charmap = make_charmap(data)
    numbers = list(parse_schematic_numbers(charmap))
    stars = parse_schematic_stars(charmap)

    # Identify engine parts
    engine_parts = [n for n in numbers if n.is_engine_part(charmap)]

    # Identify gears and populate gear ratios
    for s in stars:
        s.check_if_gear(charmap, engine_parts)
    gears = [s for s in stars if s.is_gear]

    return (
        sum([part.val for part in engine_parts]),
        sum([gear.gear_ratio for gear in gears])
    )

# Running script
fp = "2023/inputs/day3"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
