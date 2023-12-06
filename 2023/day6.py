from math import prod, sqrt, floor, ceil

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
        thold_lo = ceil( tmax/2 - sqrt((tmax/2) ** 2 - xmax))
        thold_hi = floor(tmax/2 + sqrt((tmax/2) ** 2 - xmax))
       
        # Exact integer matches are ties - must beat the previous best!
        tol = 1e-3
        x_lo = (tmax - thold_lo) * thold_lo
        x_hi = (tmax - thold_hi) * thold_hi
        if abs(x_lo - xmax) < tol:
            thold_lo += 1
        if abs(x_hi - xmax) < tol:
            thold_hi -= 1

        # Return number of integers in domain of win cases
        return (1 + thold_hi - thold_lo)
    else:
        # Quadratic has one or zero real solutions - can only tie or lose, even with perfect play
        return 0

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
