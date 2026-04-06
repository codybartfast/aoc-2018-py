#  2018 Day 12
#  ===========
#
#  Part 1: 3248
#  Part 2: 4000000000000
#
#  Timings
#  --------------------------------------
#      Parse:     0.000009s  (8.667 µs)
#     Part 1:     0.000228s  (227.9 µs)
#     Part 2:     0.003274s  (3.274 ms)
#    Elapsed:     0.003548s  (3.548 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


from collections import deque


def parse(text):

    lines = text.splitlines()
    pots = lines[0].split()[-1]

    patterns = [
        tuple(parts[0]) for line in lines[2:] if (parts := line.split())[2] == "#"
    ]
    return pots, patterns


def grow(patterns, pots):
    # assert pots[:4] == [".", ".", ".", "."]
    # assert pots[-4:] == [".", ".", ".", "."]

    quints = zip(*[pots[skip:] for skip in range(5)])
    return [
        ".",
        ".",
        *["#" if quint in patterns else "." for quint in quints],
        ".",
        ".",
    ]


def count(offset, pots):
    return sum((i - offset) if p == "#" else 0 for i, p in enumerate(pots))


def part1(data, _, __):
    start_pots, patterns = data
    patterns = set(patterns)

    size = 256
    offset = 8

    pots = ["."] * size
    pots[offset : offset + len(start_pots)] = start_pots

    for _ in range(20):
        pots = grow(set(patterns), pots)

    return count(offset, pots)


def part2(data, _, __):
    start_pots, patterns = data
    patterns = set(patterns)

    size = 512
    offset = 8

    pots = ["."] * size
    pots[offset : offset + len(start_pots)] = start_pots

    gen = 0
    prev_n_pots = count(offset, pots)
    deltas = deque(-1 for _ in range(5))

    while True:
        gen += 1
        pots = grow(patterns, pots)
        n_pots = count(offset, pots)
        delta = n_pots - prev_n_pots
        deltas.append(delta)
        prev_n_pots = n_pots
        if delta == deltas.popleft() and len(set(deltas)) == 1:
            break

    remaining_gens = 50_000_000_000 - gen
    return prev_n_pots + remaining_gens * deltas.pop()


# Runner
################################################################################


def collect_stars(text=None, filepath=None, extra_args=None):
    import workshop

    if not text and filepath:
        text = open(filepath).read().strip()
    workshop.get_cracking(text, parse, part1, part2, extra_args)


if __name__ == "__main__":
    import sys
    import workshop

    file = sys.argv[1] if len(sys.argv) > 1 else None
    filepath = workshop.get_filepath(file)
    if filepath:
        extra_args = sys.argv[2:]
        collect_stars(filepath=filepath, extra_args=extra_args)
