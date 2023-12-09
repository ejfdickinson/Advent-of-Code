def parse_sequences(data):
    return [
        [int(s) for s in line.split()]
        for line in data.splitlines()
    ]

def diff(x):
    # Of course we could use numpy, but that wouldn't be fun
    return [x[k+1]-x[k] for k in range(len(x)-1)]

def extrap_difference(sequence):
    if sequence.count(sequence[0]) < len(sequence):
        # Not all elements are the same, extrapolate recursively at both ends
        diffs = diff(sequence)
        extrap_difference(diffs)
        sequence.insert(0, sequence[0] - diffs[0])
        sequence.append(sequence[-1] + diffs[-1])

    # Else, all elements are the same
    # Extrapolation would not change the start/end, so can do nothing!

def run(data):
    sequences = parse_sequences(data)

    for sequence in sequences:
        extrap_difference(sequence)

    return (
        sum([sequence[-1] for sequence in sequences]),
        sum([sequence[0] for sequence in sequences])
    )

# Running script
fp = "2023/inputs/day9"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
