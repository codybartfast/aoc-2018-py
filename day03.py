#  2018 Day 3
#  ==========
#
#  Part 1: 115242
#  Part 2: 1046
#
#  Timings
#  --------------------------------------
#      Parse:     0.001387s  (1.387 ms)
#     Part 1:     0.016001s  (16.00 ms)
#     Part 2:     0.015591s  (15.59 ms)
#    Elapsed:     0.033024s  (33.02 ms)
#  --------------------------------------
#
#     Date:  March 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


import re


def parse(text):
    re_digits = re.compile(r"-?\d+")

    def parse_line(line):
        [id, x, y, w, h] = list(map(int, re_digits.findall(line)))
        return id, (x, y), (w, h)

    return [parse_line(line) for line in text.splitlines()]


def part1(panels, args, p1_state):
    width = height = 1000
    cloth = [0] * width * height
    for _, (x, y), (w, h) in panels:
        for row in range(y, y + h):
            start = row * width + x
            for idx in range(start, start + w):
                cloth[idx] += 1
    return sum(1 for square in cloth if square > 1)


def part2(panels, args, p1_state):
    width = height = 1000
    cloth = [0] * width * height
    candidates = set((panel[0] for panel in panels))
    for id, (x, y), (w, h) in panels:
        for row in range(y, y + h):
            start = row * width + x
            for idx in range(start, start + w):
                if cloth[idx] != 0:
                    candidates.discard(id)
                    candidates.discard(cloth[idx])
                else:
                    cloth[idx] = id
    return candidates.pop()


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
