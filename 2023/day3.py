def get_coords_adj(x,y,xmax,ymax,length=1):
    # Get list of surrounding adjacent coordinates to a (length,1) rectangle
    # with origin x,y on a grid with bounds xmax,ymax
    coords_adj = []

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

class Gear:
    def __init__(self, coord):
        self.coord = coord

    def get_nums_adj(self, charmap):
        coords_adj = []
        nums_adj = []


class Number:
    def __init__(self, s, coord_end):
        self.val = int(s)
        # Calculate digit
        x,y = coord_end
        self.length = len(s)
        self.start = (x+1-self.length, y)

    def is_engine_part(self, charmap):
        xmax = len(charmap[0])-1
        ymax = len(charmap)-1
        
        chars_adj = [
            charmap[y][x]
            for x,y in get_coords_adj(*self.start, xmax, ymax, length=self.length)
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

def parse_schematic_gears(charmap):
    for y,line in enumerate(charmap):
        for x,c in enumerate(line):
            if c == '*':
                yield Gear((x,y))

def run(data):
    charmap = make_charmap(data)

    numbers = parse_schematic_numbers(charmap)
    # gears = parse_schematic_gears(charmap)
    
    engine_parts = [n for n in numbers if n.is_engine_part(charmap)]

    return sum([part.val for part in engine_parts])

# Running script
fp = "2023/inputs/day3"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
