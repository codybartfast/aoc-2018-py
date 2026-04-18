#  2018 Day 17
#  ===========
#
#  Part 1: 33362
#  Part 2: 27801
#
#  Timings
#  --------------------------------------
#      Parse:     0.000901s  (901.3 µs)
#     Part 1:     0.017280s  (17.28 ms)
#     Part 2:     0.010761s  (10.76 ms)
#    Elapsed:     0.028991s  (28.99 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


BIG = 10**18

PERCOLATE = 0
FLOOD = 1

LEFT = -1
RIGHT = 1


def parse(text):

    def parse_line(line):
        left, right = line.split(", ")
        n = int(left[2:])
        min, max = right[2:].split("..")
        range = (int(min), int(max))
        return (n, range) if left[0] == "x" else (range, n)

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
            print(scan[x, y] if (x, y) in scan else " ", end="")
        print()


def expand(vein):
    match vein:
        case (x1, x2), y:
            return [(x, y) for x in range(x1, x2 + 1)]
        case x, (y1, y2):
            return [(x, y) for y in range(y1, y2 + 1)]


def get_scan(veins):
    return {coord: "#" for vein in veins for coord in expand(vein)}


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


def is_base(scan, pstn, dir):
    x, y = pstn
    return (
        scan.get((x, y), ".") == "#"
        or (x + dir, y) in scan
        and is_base(scan, (x + dir, y), dir)
    )


def spread(scan, pstn, dir):
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
                continue
            case "#":
                scan[x, y] = "~"
                continue
            case _:
                assert False


def flood(scan, pstn):
    if is_base(scan, pstn, LEFT) and is_base(scan, pstn, RIGHT):
        x, y = pstn
        y -= 1
        pstn = x, y
        scan[pstn] = "~"
        return spread(scan, pstn, LEFT) + spread(scan, pstn, RIGHT)


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


def mark_free_flowing(scan):
    wet = list(
        sorted(
            (pstn for pstn, val in scan.items() if val == "~"),
            key=lambda pstn: (pstn[1], pstn[0]),
        )
    )
    for x, y in wet:
        if scan.get((x - 1, y), ".") in [".", "|"]:
            scan[x, y] = "|"
    for x, y in reversed(wet):
        if scan.get((x + 1, y), ".") in [".", "|"]:
            scan[x, y] = "|"


def part1(line_defs, args, p1_state):
    scan = get_scan(line_defs)
    y_min = min(y for _, y in scan)
    y_max = max(y for _, y in scan)
    soak(scan, y_max, [(PERCOLATE, (500, 0))])
    p1_state.value = scan, y_min
    return sum(val == "~" for (_, y), val in scan.items() if y_min <= y)


def part2(data, args, p1_state):
    scan, y_min = p1_state.value
    mark_free_flowing(scan)
    return sum(val == "~" for (_, y), val in scan.items() if y_min <= y)


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
