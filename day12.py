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
    assert pots[:4] == [".", ".", ".", "."]
    assert pots[-4:] == [".", ".", ".", "."]

    quints = zip(*[pots[s:] for s in range(5)])
    return [
        ".",
        ".",
        *["#" if quint in patterns else "." for quint in quints],
        ".",
        ".",
    ]


def count(offset, pots):
    return sum((i - offset) if p == "#" else 0 for i, p in enumerate(pots))


def part1(data, args, p1_state):
    # print(f"\n{data}\n")
    start_pots, patterns = data
    size = 200
    offset = 20

    pots = ["."] * size
    pots[offset : offset + len(start_pots)] = start_pots

    for _ in range(20):
        pots = grow(set(patterns), pots)

    return count(offset, pots)


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
