class MessageQueue:
    modules = {}
    queue = []
    low_count = 0
    high_count = 0
    active = False

    @staticmethod
    def reset():
        MessageQueue.low_count = 0
        MessageQueue.high_count = 0

        for module in MessageQueue.modules.values():
            module.reset()

    @staticmethod
    def parse_modules(data):
        MessageQueue.modules["button"] = Button("button", "broadcaster")

        for line in data.splitlines():
            id, dst = line.split(" -> ")
            dst = dst.split(", ")

            if id == "broadcaster":
                MessageQueue.modules[id] = Broadcast(id, dst)
            elif id[0] == "%":
                id = id[1:]
                MessageQueue.modules[id] = FlipFlop(id, dst)
            elif id[0] == "&":
                id = id[1:]
                MessageQueue.modules[id] = Conjunction(id, dst) 

        # Map the source nodes for Conjunction types
        for id, module in MessageQueue.modules.items():
            if isinstance(module, Conjunction):
                src = []
                for id_src, module_src in MessageQueue.modules.items():
                    if id in module_src.dst:
                        src.append(id_src)
                module.src = src

        # Check for output nodes
        for module in MessageQueue.modules.copy().values():
            for id_dst in module.dst:
                if id_dst not in MessageQueue.modules:
                    MessageQueue.modules[id_dst] = Module(id_dst, [])

        MessageQueue.reset()

    @staticmethod
    def add(src, dst, state):
        MessageQueue.queue.append((src, dst, state))
        
    @staticmethod
    def run(check_active=False):
        while len(MessageQueue.queue) > 0:
            src, dst, state = MessageQueue.queue.pop(0)

            if check_active and dst == "rx" and not state:
                MessageQueue.active = True
                break

            if state:
                MessageQueue.high_count += 1
            else:
                MessageQueue.low_count += 1
            MessageQueue.modules[dst].handle(src, state)

class Module:
    def __init__(self, id, dst):
        self.id = id
        self.dst = dst

        if not isinstance(self.dst, list):
            self.dst = [self.dst]

    def reset(self):        
        self.state = False

    def broadcast(self, state):
        for node in self.dst:
            MessageQueue.add(self.id, node, state)

    def handle(self, src, pulse):
        pass

class FlipFlop(Module):
    def handle(self, src, pulse):
        if not pulse:
            self.state = (not self.state)
            self.broadcast(self.state)

class Conjunction(Module):
    def reset(self):
        self.state = { k: False for k in self.src }

    def handle(self, src, pulse):
        self.state[src] = pulse
        self.broadcast(not all(self.state.values()))

class Broadcast(Module):
    def handle(self, src, pulse):
        self.broadcast(pulse)

class Button(Module):
    def handle(self, src, pulse):
        self.broadcast(False)

def run(data):
    MessageQueue.parse_modules(data)

    n_pushes = 1000
    for i in range(n_pushes):    
        # Push button
        MessageQueue.add("button", "broadcaster", False)
        MessageQueue.run()

    count = MessageQueue.low_count * MessageQueue.high_count
    MessageQueue.reset()

    n_pushes_to_active = 0
    while not MessageQueue.active:
        # Push button
        n_pushes_to_active += 1
        MessageQueue.add("button", "broadcaster", False)
        MessageQueue.run(check_active=True)
            
    return (
        count,
        n_pushes_to_active
    )

# Running script
fp = "2023/inputs/day20"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
