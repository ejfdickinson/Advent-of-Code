# TODO(ED): deal with memory / run-time inefficiency

from copy import deepcopy

class Space:
    def __init__(self, data):
        self.components, self.size = Space.parse_components(data)
        self.energized = set()
        self.mapped = set()

    @staticmethod
    def parse_components(data):
        lines = data.splitlines()

        xmax = len(lines[0])
        ymax = len(lines)

        components = {}
        for y,line in enumerate(lines):
            for x,c in enumerate([*line]):
                if c != '.':
                    components[(x,y)] = c

        return components, (xmax, ymax)

    def trace_ray(self, u, v):
        if (u,v) in self.mapped:
            # Ray has already been traced
            return
        else:
            self.mapped.add((u, v))
        
        ray = Ray(u, v)
        
        tracing = True
        while tracing:
            v_new = ray.step(self.components)
            loc = (ray.u, ray.v)
            if loc in self.mapped or not ray.in_bounds(self.size):
                # Has already been traced, done
                tracing = False
            else:
                self.mapped.add(loc)
            
            if v_new:
                self.trace_ray(ray.u, v_new)
                
            if tracing:
                self.energized.add(ray.u)

class Ray:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def in_bounds(self, size):
        x, y = self.u
        xmax, ymax = size
    
        return (x >= 0 and x < xmax and y >= 0 and y < ymax)

    def step(self, components):
        # Return velocity of new ray spawned, if any. Otherwise, return None.

        # Advance ray
        x,y = self.u
        vx,vy = self.v
        self.u = (x + vx, y + vy)

        # Update velocity in case of collision
        if self.u in components:
            if components[self.u] == '\\':
                self.v = (vy, vx)
            elif components[self.u] == '/':
                self.v = (-vy, -vx)
            elif components[self.u] == '-' and vx == 0:
                self.v = (-1,0)
                return (1,0)        
            elif components[self.u] == '|' and vy == 0:
                self.v = (0,1)
                return (0,-1)

        return None


def run(data):
    space = Space(data)
    xmax, ymax = space.size

    start_configs = []
    # Left-hand side
    start_configs.extend([
        ((-1, y), (1, 0)) for y in range(ymax)
    ])
    # Top side
    start_configs.extend([
        ((x, -1), (0, 1)) for x in range(xmax)
    ])
    # Right-hand side
    start_configs.extend([
        ((xmax, y), (-1, 0)) for y in range(ymax)
    ])
    # Bottom side
    start_configs.extend([
        ((x, ymax), (0, -1)) for x in range(xmax)
    ])

    spaces = {
        start_config: deepcopy(space) for start_config in start_configs
    }

    energized = []
    for start_config, space in spaces.items():       
        space.trace_ray(*start_config)
        energized.append(len(space.energized))

    return (
        energized[0],
        max(energized)
    )

# Running script
fp = "2023/inputs/day16"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
