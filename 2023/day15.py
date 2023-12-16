def parse_initialization(s, raw=False):
    steps = s.rstrip().split(',')
    if raw:
        return steps
    else:
        return [parse_step(step) for step in steps]

def parse_step(s):
    if '=' in s:
        return s.partition('=')
    else:
        return s.partition('-')

def hash(s):
    val = 0
    for c in [*s]:
        val += ord(c)
        val *= 17
        val %= 256

    return val

def run_instructions(instructions):
    boxes = [[] for i in range(256)]
    focal_lengths = {}

    for label,op,val in instructions:
        boxid = hash(label)

        if op == '-':
            try:
                boxes[boxid].remove(label)
            except ValueError:
                pass
        elif op == '=':
            focal_lengths[label] = int(val)
            if not label in boxes[boxid]:
                boxes[boxid].append(label)
        else:
            raise RuntimeError("Bad operation")
        
    return boxes, focal_lengths

def get_focusing_power(box_contents, focal_lengths):
    focusing_power = 0
    for boxid,box in enumerate(box_contents):
        for slot,lens in enumerate(box):
            focusing_power += (
                (boxid + 1) * (slot + 1) * focal_lengths[lens]
            )

    return focusing_power

def run(data):
    hash_sum = sum(hash(step) for step in parse_initialization(data, raw=True))

    instructions = parse_initialization(data)
    boxes, focal_lengths = run_instructions(instructions)

    return (
        hash_sum,
        get_focusing_power(boxes, focal_lengths)
    )

# Running script
fp = "2023/inputs/day15"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
