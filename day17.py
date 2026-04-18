BIG = 10**18

PERCOLATE = 0
FLOOD = 1

LEFT = -1
RIGHT = 1


def parse(text):

    def parse_line(line):
        h1, h2 = line.split(", ")
        n = int(h1[2:])
        min, max = h2[2:].split("..")
        range = (int(min), int(max))
        return (n, range) if h1[0] == "x" else (range, n)

    return [parse_line(line) for line in text.splitlines()]


def display(scan):
    print()

    x_min = min(x for x, _ in scan)
    x_max = max(x for x, _ in scan)
    y_min = 0
    y_max = max(y for _, y in scan)

    for y in range(y_min, y_max + 1):
        print(f"{y:4} ", end="")
        for x in range(x_min, x_max + 1):
            print(scan[x, y].replace("#", "█") if (x, y) in scan else " ", end="")
        print()


def expand(layer):
    match layer:
        case (x1, x2), y:
            return [(x, y) for x in range(x1, x2 + 1)]
        case x, (y1, y2):
            return [(x, y) for y in range(y1, y2 + 1)]


def get_scan(layers):
    coords = [coord for layer in layers for coord in expand(layer)]
    scan = {coord: "#" for coord in coords}
    return scan


def percolate(scan, y_max, pstn):

    x, y = pstn
    y += 1
    pstn = x, y

    if y > y_max:
        return []

    if pstn not in scan:
        scan[x, y] = "~"
        return [(PERCOLATE, pstn)]

    return [(FLOOD, pstn)]

    return []


def is_base(scan, pstn, dir):
    x, y = pstn
    return (
        scan.get((x, y), ".") == "#"
        or (x + dir, y) in scan
        and is_base(scan, (x + dir, y), dir)
    )


def flow(scan, pstn, dir):
    x, y = pstn

    while True:
        x += dir
        if scan.get((x, y), ".") == "#":
            return []
        match scan.get((x, y + 1), "."):
            case ".":
                if scan[x - dir, y + 1] == "#":
                    scan[x, y] = "~"
                    return [(PERCOLATE, (x, y))]
                else:
                    return []
            case "~":
                scan[x, y] = "~"
                # print("~")
                continue
            case "#":
                scan[x, y] = "~"
                # print("#")
                continue
            case _:
                assert False


def flood(scan, pstn):
    if is_base(scan, pstn, LEFT) and is_base(scan, pstn, RIGHT):
        x, y = pstn
        y -= 1
        pstn = x, y
        scan[pstn] = "~"
        return flow(scan, pstn, LEFT) + flow(scan, pstn, RIGHT)


def seep(scan, y_max, trickle):
    dir, pstn = trickle
    x, y = pstn

    if dir == PERCOLATE:
        return percolate(scan, y_max, pstn)
    else:
        match flood(scan, pstn):
            case None:
                return []
            case []:
                return [(FLOOD, (x, y - 1))]
            case trickles:
                return trickles


def soak(scan, y_max, trickles):
    while trickles:
        trickles = [
            new_trickle
            for trickle in trickles
            for new_trickle in seep(scan, y_max, trickle)
        ]


def part1(line_defs, args, p1_state):
    scan = get_scan(line_defs)
    y_min = min(y for _, y in scan)
    y_max = max(y for _, y in scan)
    soak(scan, y_max, [(PERCOLATE, (500, 0))])
    # display(scan)
    return sum(val == "~" for (_, y), val in scan.items() if y_min <= y)


def part2(data, args, p1_state):
    return "ans2"


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
