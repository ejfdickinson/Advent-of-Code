class Number:
    def __init__(self, s, coord_end):
        self.val = int(s)
        # Calculate digit
        x,y = coord_end
        self.coord_start = (x+1-len(s), y)
        self.coord_end   = coord_end

    def is_engine_part(self, charmap):
        chars_adj = ''

        xstart,y = self.coord_start
        xend,_ = self.coord_end

        xmax = len(charmap)-1
        ymax = len(charmap[0])-1

        # Adjacent chars (cardinal directions)
        if y > 0:
            chars_adj += ''.join(charmap[y-1][xstart:xend+1])
        if y < ymax:
            chars_adj += ''.join(charmap[y+1][xstart:xend+1])
        if xstart > 0:
            chars_adj += charmap[y][xstart-1]
        if xend < xmax:
            chars_adj += charmap[y][xend+1]

        # Adjacent chars (diagonal directions)
        if y > 0:
            if xstart > 0:
                chars_adj += charmap[y-1][xstart-1]
            if xend < xmax:
                chars_adj += charmap[y-1][xend+1]
        if y < ymax:
            if xstart > 0:
                chars_adj += charmap[y+1][xstart-1]
            if xend < xmax:
                chars_adj += charmap[y+1][xend+1]

        return any(c != '.' for c in chars_adj)       

def make_charmap(data):
    return [[*line] for line in data.splitlines()]

def parse_schematic(charmap):
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

def run(data):
    charmap = make_charmap(data)
    numbers = parse_schematic(charmap)
    engine_parts = [n for n in numbers if n.is_engine_part(charmap)]

    return sum([part.val for part in engine_parts])

# Running script
fp = "2023/inputs/day3"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
