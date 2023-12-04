import re

def parse_scratchcards(data):
    line_parts = [tuple(re.split(r":|\|", line)) for line in data.splitlines()]

    games = [
        ([int(s) for s in wins.split()],[int(s) for s in nums.split()])
        for _,wins,nums in line_parts
    ]

    return games

def get_matches(a, b):
    return set(a).intersection(set(b))

def run(data):
    games = parse_scratchcards(data)
    matches_by_game = [get_matches(winning_numbers, card_numbers) for winning_numbers, card_numbers in games]
    point_scores = [2 ** (len(match)-1) if len(match) > 0 else 0 for match in matches_by_game]

    return sum(point_scores)

# Running script
fp = "2023/inputs/day4"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
