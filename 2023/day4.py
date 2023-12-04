import re

def parse_scratchcards(data):
    line_parts = [tuple(re.split(r":|\|", line)) for line in data.splitlines()]

    games = [
        ([int(s) for s in wins.split()],[int(s) for s in nums.split()])
        for _,wins,nums in line_parts
    ]

    return games

def count_matches(a, b):
    return len(set(a).intersection(set(b)))

def get_score(n):
    if n > 0:
        return (2 ** (n-1))
    else:
        return 0

def run(data):
    games = parse_scratchcards(data)
    match_counts = [
        count_matches(winning_numbers, card_numbers)
        for winning_numbers, card_numbers in games
    ]

    point_scores = [get_score(n) for n in match_counts]

    return sum(point_scores)

# Running script
fp = "2023/inputs/day4"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
