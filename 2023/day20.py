def link_modules(a, b):
    a.dst.append(b)
    b.src.append(a)

class MessageQueue:
    modules = {}
    queue = []
    low_count = 0
    high_count = 0

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
                module.set_initial_state()

        # Check for output nodes
        for module in MessageQueue.modules.copy().values():
            for id_dst in module.dst:
                if id_dst not in MessageQueue.modules:
                    MessageQueue.modules[id_dst] = Module(id_dst, [])

    @staticmethod
    def add(src, dst, state):
        MessageQueue.queue.append((src, dst, state))
        
    @staticmethod
    def run():
        while len(MessageQueue.queue) > 0:
            src, dst, state = MessageQueue.queue.pop(0)
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
    def set_initial_state(self):
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

    return (
        MessageQueue.low_count * MessageQueue.high_count,
    )

# Running script
fp = "2023/inputs/day20"
with open(fp) as file:
    data = file.read()

output = run(data)
print(output)
