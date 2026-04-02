#  2018 Day 5
#  ==========
#
#  Part 1: 11194
#  Part 2: 4178
#
#  Timings
#  --------------------------------------
#      Parse:     0.000002s  (2.375 µs)
#     Part 1:     0.002767s  (2.767 ms)
#     Part 2:     0.071588s  (71.59 ms)
#    Elapsed:     0.074396s  (74.40 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


def parse(text):
    return text.encode()


def react(polymer, strip=0):
    reduced = []
    idx = 0
    l_poly = len(polymer)

    while idx < l_poly:
        if ((unit := polymer[idx]) & 0b1011111) != strip:
            reduced.append(unit)
        idx += 1
        while reduced and idx < l_poly and reduced[-1] ^ polymer[idx] == 32:
            reduced.pop()
            idx += 1

    return reduced


def part1(polymer, args, p1_state):
    return len(react(polymer))


def part2(polymer, args, p1_state):
    return min(len(react(polymer, type)) for type in set(polymer.upper()))


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
