# Naive approaches will not work for Day 5b!

def parse_data(input):
    input_parts = input.split("\n\n")

    seeds = [int(s) for s in input_parts[0].split()[1:]]
    
    maps = [
        [
            [int(s) for s in line.split()]
            for line in part.splitlines()[1:]
        ]
        for part in input_parts[1:]
    ]
    
    return seeds, maps

def process_map(loc, mapping):
    for section in mapping:
        # Maps are listed as: destination start, source start, range length
        dst, src, length = section

        if loc >= src and loc < (src+length):
            return loc + (dst - src)
        
    # Else not in the explicitly mapped sections
    return loc

def process_inverse_map(seed, mapping):
    for section in mapping:
        # Maps are listed as: destination start, source start, range length
        # Treat as one-to-one inverse, so src = dst, dst = src
        src, dst, length = section

        if seed >= src and seed < (src+length):
            return seed + (dst - src)
        
    # Else not in the explicitly mapped sections
    return seed

def get_locations(seeds, maps):
    locs = seeds
    for mapping in maps:
        locs = [process_map(loc, mapping) for loc in locs]
    
    return locs

def get_seed(loc, maps):
    seed = loc
    for mapping in reversed(maps):
        seed = process_inverse_map(seed, mapping)
        
    return seed

def is_seed(val, seedvals, read_as_pairs=True):
    if read_as_pairs:
        for i in range(len(seedvals) // 2):
            relval = val - seedvals[2*i]
            if relval >= 0 and relval < seedvals[2*i + 1]:
                return True
        
        # Else not found
        return False
    else:
        return (val in seedvals)

def get_minloc(seedvals, maps, read_as_pairs=True):
    loc = 0
    while not is_seed(get_seed(loc, maps), seedvals, read_as_pairs=read_as_pairs):
        loc += 1

    return loc

def run(data):
    seedvals, maps = parse_data(data)
    
    return (
        get_minloc(seedvals, maps, read_as_pairs=False),
        # min(locations2)
    )

# Running script
fp = "2023/inputs/day5_test"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
