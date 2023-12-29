class Hailstone():
    def __init__(self, u0, v):
        self.u0 = u0
        self.v  = v


class Intersection2D():
    def __init__(self, u, t1, t2):
        self.u = u
        self.t1 = t1
        self.t2 = t2


def parse_hail(data):
    str_hail = [
        line.split(' @ ') for line in data.splitlines()
    ]

    hailstones = [
        Hailstone(
            [float(x) for x in hail[0].split(',')],
            [float(x) for x in hail[1].split(',')]
        )
        for hail in str_hail
    ]

    return hailstones


def get_2d_path_intersections(hailstones, xmin, xmax, ymin, ymax):
    intersections = {}

    for i,stone1 in enumerate(hailstones):
        for j,stone2 in enumerate(hailstones[i+1:]):
            intersection = intersect_2D_path(stone1, stone2)

            if intersection is None:
                # Parallel paths
                continue

            x, y = intersection.u

            if (
                intersection.t1 >= 0 and intersection.t2 >= 0 and
                x >= xmin and x <= xmax and y >= ymin and y <= ymax
            ):
                # In future and in bounds
                intersections[(i,i+j+1)] = intersection

    return intersections


def intersect_2D_path(stone1, stone2):
    # Returns an Intersection2D if non-parallel, else None for parallel lines

    ux1, uy1, _ = stone1.u0
    ux2, uy2, _ = stone2.u0

    vx1, vy1, _ = stone1.v
    vx2, vy2, _ = stone2.v

    # Parametric path:
    #   y = uy + vy * t
    #   x = ux + vx * t
    # Non-parametric path:
    #   y = uy + grad * (x - ux)
    #       where grad = vy / vx

    # Solve for x1 = x2, y1 = y2
    # x = ((uy1 - uy2) + grad2 * ux2 - grad1 * ux1) / (grad2 - grad1)
    
    grad1 = vy1 / vx1
    grad2 = vy2 / vx2
    
    if grad1 == grad2:
        # Parallel
        return None

    x = ((uy1 - uy2) + grad2 * ux2 - grad1 * ux1) / (grad2 - grad1)
    t1 = (x - ux1) / vx1
    t2 = (x - ux2) / vx2
    y = uy1 + vy1 * t1
    
    return Intersection2D((x, y), t1, t2)


def get_magic_hailstone(hailstones):
    # Find the initial position and velocity that will collide with every hailstone
    pass

def run(data):
    hailstones = parse_hail(data)

    lo = 200000000000000
    hi = 400000000000000

    intersections = get_2d_path_intersections(hailstones, lo, hi, lo, hi)

    pos, _ = get_magic_hailstone(hailstones)

    return (
        len(intersections),
        sum(pos)
    )

# Running script
fp = "2023/inputs/day24"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
