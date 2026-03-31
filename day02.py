#  ==========
#
#  Part 1: 5681
#  Part 2: uqyoeizfvmbistpkgnocjtwld
#
#  Timings
#  --------------------------------------
#      Parse:     0.000009s  (9.000 µs)
#     Part 1:     0.000330s  (329.8 µs)
#     Part 2:     0.012288s  (12.29 ms)
#    Elapsed:     0.012664s  (12.66 ms)
#  --------------------------------------
#
#     Date:  March 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


from collections import Counter


def parse(text):
    return text.splitlines()


def part1(ids, args, p1_state):
    n_two = 0
    n_three = 0
    for id in ids:
        counts = Counter(id)
        n_two += 2 in counts.values()
        n_three += 3 in counts.values()
    return n_two * n_three


def part2(ids, args, p1_state):
    for i, id1 in enumerate(ids):
        for id2 in ids[i + 1 :]:
            diff_count = sum(c1 != c2 for c1, c2 in zip(id1, id2))
            if diff_count == 1:
                return "".join(c1 for c1, c2 in zip(id1, id2) if c1 == c2)


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
