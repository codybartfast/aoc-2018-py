#  2018 Day 7
#  ==========
#
#  Part 1: BDHNEGOLQASVWYPXUMZJIKRTFC
#  Part 2: 1107
#
#  Timings
#  --------------------------------------
#      Parse:     0.000027s  (26.96 µs)
#     Part 1:     0.000057s  (57.00 µs)
#     Part 2:     0.000062s  (62.25 µs)
#    Elapsed:     0.000181s  (181.2 µs)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


def parse(text):
    def parse_line(line):
        parts = line.split()
        return (parts[1], parts[7])

    return [parse_line(line) for line in text.splitlines()]


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
    done = []

    while len(done) < n_steps:
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
            done.append(step)
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
