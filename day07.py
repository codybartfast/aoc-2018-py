import re


def parse(text):
    re_digits = re.compile(r"-?\d+")

    def parse_line(line):
        parts = line.split()
        return (parts[1], parts[7])

    lines = text.splitlines()
    return [parse_line(line) for line in lines]


def relations(instructions):
    instructions.sort(key=lambda kvp: kvp[1])
    all_steps = list(sorted(set(step for instr in instructions for step in instr)))
    supports = {step: [] for step in all_steps}
    requires = {step: [] for step in all_steps}
    for a, b in instructions:
        supports[a].append(b)
        requires[b].append(a)
    return supports, requires


def part1(instructions, args, p1_state):
    supports, requires = relations(instructions)

    steps = []
    for _ in range(len(supports)):
        step = [key for key, val in requires.items() if not val][0]
        requires.pop(step)
        for dependent in supports[step]:
            requires[dependent].remove(step)
        steps.append(step)
    return "".join(steps)


def part2(instructions, args, p1_state):
    time_const = 60
    free_elves = 5

    supports, requires = relations(instructions)

    n_steps = len(supports)
    in_progress = {}
    time = 0
    steps = []

    while len(steps) < n_steps:
        while free_elves and (
            available := [step for step, reqs in requires.items() if not reqs]
        ):
            step = available[0]
            requires.pop(step)
            free_elves -= 1
            finish_time = time + time_const + ord(step) - 0x40
            in_progress.setdefault(finish_time, []).append(step)

        time = min(in_progress)
        completed = in_progress[time]
        in_progress.pop(time)
        for step in completed:
            steps.append(step)
            free_elves += 1
            for dependent in supports[step]:
                requires[dependent].remove(step)

    return time


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
