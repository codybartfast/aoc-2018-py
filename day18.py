#  2018 Day 18
#  ===========
#
#  Part 1: 519552
#  Part 2: 165376
#
#  Timings
#  --------------------------------------
#      Parse:     0.000027s  (27.17 µs)
#     Part 1:     0.007619s  (7.619 ms)
#     Part 2:     0.401667s  (401.7 ms)
#    Elapsed:     0.409360s  (409.4 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


def parse(text):
    lines = text.splitlines()
    width = len(lines) + 2
    parts = ["."] * width
    for line in lines:
        parts.append(".")
        parts.extend(list(line))
        parts.append(".")
    parts.extend(["."] * width)

    return width, parts


def value(terra):
    return terra.count("|") * terra.count("#")


def minute(width, terra):
    tnova = ["."] * (width * width)
    for y in range(1, width - 1):
        for x in range(1, width - 1):
            pstn = y * width + x
            n_open = 0
            n_tree = 0
            n_yard = 0
            for adj in [
                pstn - width - 1,
                pstn - width,
                pstn - width + 1,
                pstn - 1,
                pstn + 1,
                pstn + width - 1,
                pstn + width,
                pstn + width + 1,
            ]:
                match terra[adj]:
                    case ".":
                        n_open += 1
                    case "|":
                        n_tree += 1
                    case "#":
                        n_yard += 1
            match terra[pstn]:
                case ".":
                    tnova[pstn] = "|" if n_tree >= 3 else "."
                case "|":
                    tnova[pstn] = "#" if n_yard >= 3 else "|"
                case "#":
                    tnova[pstn] = "#" if n_tree and n_yard else "."
    return tnova


def part1(data, args, p1_state):
    width, terra = data

    for _ in range(10):
        terra = minute(width, terra)

    return value(terra)


def part2(data, args, p1_state):
    width, terra = data
    prelude = 512

    for _ in range(prelude):
        terra = minute(width, terra)

    values = []
    while True:
        terra = minute(width, terra)
        val = value(terra)
        values.append(val)
        if values.count(val) == 2:
            break

    val = values[-1]
    pstns = [i for i, v in enumerate(values) if v == val]
    period = pstns[1] - pstns[0]
    remaining = (1_000_000_000 - len(values) - prelude) % period

    for _ in range(remaining):
        terra = minute(width, terra)

    return value(terra)


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
