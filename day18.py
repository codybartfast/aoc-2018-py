from array import array


def parse(text):
    lines = text.splitlines()
    assert len(lines) == len(lines[0])
    width = len(lines) + 2
    parts = []
    parts.extend(["."] * width)
    for line in lines:
        parts.append(".")
        parts.extend(list(line))
        parts.append(".")
    parts.extend(["."] * width)

    return width, parts


def display(width, terra):
    print()
    for start in range(0, width * width, width):
        print("".join(terra[start : start + width]))
    print()


def value(terra):
    return terra.count("|") * terra.count("#")


def terranova(width):
    return ["."] * (width * width)


def minute(width, terra):
    tnova = terranova(width)
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
        v = value(terra)
        values.append(v)
        if values.count(v) == 2:
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
