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

def get_n_cards(match_counts):
    # Generate new cards in order, starting with one of each.
    # Done very literally! Based on our knowing we never having to backtrack.
    n_games = len(match_counts)
    n_cards = [1] * n_games
    for k,n in enumerate(match_counts):
        for i in id_newcards(k, n, n_games):
            # Edit in place - guaranteed that (i > k)
            # n_k copies of card k already obtained
            n_cards[i] += n_cards[k]
    
    return n_cards

def id_newcards(base, n, maxval):
    return range(base + 1, min(base + n + 1, maxval))

def run(data):
    games = parse_scratchcards(data)
    match_counts = [
        count_matches(winning_numbers, card_numbers)
        for winning_numbers, card_numbers in games
    ]

    point_scores = [get_score(n) for n in match_counts]
    n_cards = get_n_cards(match_counts)

    return (
        sum(point_scores),
        sum(n_cards)
    )

# Running script
fp = "2023/inputs/day4"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
