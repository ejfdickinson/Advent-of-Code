import re
from math import prod

COL_STRINGS = [" red", " green", " blue"]

def get_game_maxvals(line):
    vals = [
        [int(s.replace(col,"")) for s in re.findall(r"[0-9]*" + col,line)]
        for col in COL_STRINGS
    ]

    game_maxvals = [max(val) if len(val) > 0 else 0 for val in vals]
    return game_maxvals


def is_possible(maxvals, max_allowed):
    return all(val <= allowed for val,allowed in zip(maxvals,max_allowed))

def get_possible(game_maxvals, max_allowed):
    good_games = [
        (k+1) for k,maxvals in enumerate(game_maxvals)
        if is_possible(maxvals, max_allowed)
    ]
    return good_games

def get_powers(game_maxvals):
    return [prod(maxvals) for maxvals in game_maxvals]

def run(data):
    game_maxvals = [get_game_maxvals(line) for line in data.splitlines()]
    good_games = get_possible(game_maxvals, (12,13,14))
    powers = get_powers(game_maxvals)

    return (sum(good_games), sum(powers))

# Running script
fp = "2023/inputs/day2"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
