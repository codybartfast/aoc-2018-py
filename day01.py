#  2018 Day 1
#  ==========
#
#  Part 1: 561
#  Part 2: 563
#
#  Timings
#  --------------------------------------
#      Parse:     0.000077s  (77.04 µs)
#     Part 1:     0.000006s  (6.000 µs)
#     Part 2:     0.007108s  (7.108 ms)
#    Elapsed:     0.007226s  (7.226 ms)
#  --------------------------------------
#
#     Date:  March 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


def parse(text):
    return [int(line) for line in text.splitlines()]


def part1(changes, args, p1_state):
    return sum(changes)


def part2(changes, args, p1_state):
    l_changes = len(changes)
    seen = set()
    idx = freq = 0
    while freq not in seen:
        seen.add(freq)
        freq += changes[idx]
        idx = (idx + 1) % l_changes
    return freq


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
