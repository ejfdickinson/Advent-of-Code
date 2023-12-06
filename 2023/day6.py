from math import prod, sqrt, floor, ceil, modf

def parse_races(data, read_properly=True):
    if read_properly:
        # Return a tuple (tmax, xmax)
        times, distances = [
            int(''.join(line.split()[1:]))
            for line in data.splitlines()
        ]

        return (times, distances)
    else:
        # Return a list of tuples (tmax, xmax)
        times, distances = [
            [int(s) for s in line.split()[1:]]
            for line in data.splitlines()
        ]

        return zip(times, distances)

def count_winning_methods(race):
    tmax, xmax = race

    # tmax = thold + trun
    # u = 1.0 * thold
    # x = u * trun

    # x > xmax where:
    #   u * trun > xmax
    #   thold * trun > xmax
    #   thold * (tmax - thold) > xmax

    # Tie with existing best occurs at roots of quadratic:
    #   thold * (thold - tmax) + xmax = 0
    # with solution:
    #   thold = tmax/2 +/- sqrt((tmax/2)^2 - xmax)

    if (0.25 * tmax * tmax) > xmax:
        # Quadratic has two real solutions - win cases are in the finite range between them

        # Get analytical solutions, rounded to closest integers
        half_range = sqrt((tmax/2) ** 2 - xmax)
        thold_lo = fine_tune(tmax/2 - half_range, *race, assume_above=False)
        thold_hi = fine_tune(tmax/2 + half_range, *race, assume_above=True)

        # Return number of integers in domain of win cases
        return (1 + thold_hi - thold_lo)
    else:
        # Quadratic has one or zero real solutions - can only tie or lose, even with perfect play
        return 0

def fine_tune(tfloat, tmax, xmax, assume_above=True):
    # For tfloat a root of tfloat * (tmax - tfloat) - xmax = 0,
    # find nearest adjacent integer for which tfloat * (tmax - tfloat) > xmax

    tfrac, tint = modf(tfloat)
    if tfrac > 1e-10:
        # Not an integer solution, use our intuition to know which side to round
        if assume_above:
            return floor(tfloat)
        else:
            return ceil(tfloat)
    else:
        # Seems likely that there is an integer tie, find the integer solution
        for val in [tint-1, tint, tint+1]:
            if val * (tmax - val) > xmax:
                return val

def run(data):
    bad_races = parse_races(data, read_properly=False)
    good_race = parse_races(data)

    nwins_bad = [count_winning_methods(race) for race in bad_races]
    nwins_good = count_winning_methods(good_race)

    return (
        prod(nwins_bad),
        nwins_good
    )

# Running script
fp = "2023/inputs/day6"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
