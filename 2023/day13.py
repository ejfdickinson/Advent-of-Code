def parse_patterns(data):
    pattern_strings = data.split("\n\n")

    pattern_rows = [
        pattern_string.splitlines()
        for pattern_string in pattern_strings
    ]

    pattern_cols = [
        [
            ''.join([pattern_row[y][x] for y in range(len(pattern_row))])
            for x in range(len(pattern_row[0]))
        ]
        for pattern_row in pattern_rows
    ]

    return list(zip(pattern_rows,pattern_cols))

def match_rowcol(pattern):
    rows,cols = pattern

    matchrow = None
    matchcol = None

    for y in range(len(rows)-1):
        if is_reflected(rows, y):
            matchrow = y+1
            break

    for x in range(len(cols)-1):
        if is_reflected(cols, x):
            matchcol = x+1
            break

    return matchrow,matchcol

def is_reflected(lines, n):
    ntot = len(lines)
    if n == ntot:
        return False

    nreflect = n+1
    while n >= 0 and nreflect < len(lines):
        if (lines[n] != lines[nreflect]):
            return False
        else:
            n -= 1
            nreflect += 1
    
    return True

def run(data):
    patterns = parse_patterns(data)
    matches = [match_rowcol(pattern) for pattern in patterns]
    summaries = [(matchcol or 0) + 100 * (matchrow or 0) for matchrow,matchcol in matches]

    return (
        sum(summaries),
    )

# Running script
fp = "2023/inputs/day13"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
