from collections import deque


def parse(text):

    def parse_line(line):
        parts = line.split()
        if parts[2] == "#":
            return parts[0]

    lines = text.splitlines()
    pots = lines[0].split()[-1]
    patterns = []
    for line in lines[2:]:
        parts = line.split()
        if parts[2] == "#":
            patterns.append(tuple(parts[0]))
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
    # print(f"\n{data}\n")
    start_pots, patterns = data
    patterns = set(patterns)

    size = 200
    offset = 20

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
