import re

def parse(text):
    re_digits = re.compile(r"-?\d+")

    def parse_line(line):
        parts = line.split()
        return (parts[1], parts[7])

    lines = text.splitlines()
    return [parse_line(line) for line in lines]


def part1(data, args, p1_state):
    data.sort(key=lambda kvp: kvp[1])
    all_steps = list(sorted(set(step for instr in data for step in instr)))
    supports = {step: [] for step in all_steps}
    requires = {step: [] for step in all_steps}
    for a,b in data:
        supports[a].append(b)
        requires[b].append(a)

    steps = []
    for _ in range(len(all_steps)):
        step = [key for key, val in requires.items() if not val][0]
        requires.pop(step)
        for dependency in supports[step]:
            requires[dependency].remove(step)
        steps.append(step)
    return "".join(steps)


def part2(data, args, p1_state):
    return "ans2"


# Runner
################################################################################


def collect_stars(text=None, filepath=None, extra_args=None):
    import workshop as ws
    
    if not text and filepath:
        text = open(filepath).read().strip()
    ws.get_cracking(text, parse, part1, part2, extra_args)


if __name__ == "__main__":
    import sys
    import workshop as ws

    file = sys.argv[1] if len(sys.argv) > 1 else None
    filepath = ws.get_filepath(file)
    if filepath:
        extra_args = sys.argv[2:]
        collect_stars(filepath=filepath, extra_args=extra_args)
