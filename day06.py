#  2018 Day 6
#  ==========
#
#  Part 1: 4233
#  Part 2: 45290
#
#  Timings
#  --------------------------------------
#      Parse:     0.000015s  (14.79 µs)
#     Part 1:     0.056734s  (56.73 ms)
#     Part 2:     0.112467s  (112.5 ms)
#    Elapsed:     0.169269s  (169.3 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


# Part 1 is a bit more complicated than necesary because the more brute force
# approch (see earlier commits) was taking > 400ms which seemed excessive.

from collections import Counter


def parse(text):
    def parse_line(line):
        parts = line.split(", ")
        return int(parts[0]), int(parts[1])

    return [parse_line(line) for line in text.splitlines()]


def part1(coords, args, p1_state):
    min_x = min(x for x, y in coords)
    max_x = max(x for x, y in coords)
    min_y = min(y for x, y in coords)
    max_y = max(y for x, y in coords)

    p1_state.value = (min_x + max_x) // 2, (min_y + max_y) // 2

    areas = [[coord, set([coord]), set([coord])] for coord in coords]
    claims = {coord: coord for coord in coords}
    new_claims = {None: None}
    while new_claims:
        new_claims.clear()
        for area in areas:
            coord, known, edge = area
            new_edge = set()
            for xy in [
                (nx, ny)
                for ex, ey in edge
                for nx, ny in [(ex, ey - 1), (ex + 1, ey), (ex, ey + 1), (ex - 1, ey)]
                if (nx, ny) not in known
            ]:
                if xy not in claims:
                    if min_x <= xy[0] <= max_x and min_y <= xy[1] <= max_y:
                        new_edge.add(xy)
                        known.add(xy)
                        claims[xy] = coord
                        new_claims[xy] = coord
                else:
                    if xy in new_claims and new_claims[xy] != coord:
                        claims[xy] = None
            area[2] = new_edge

    return Counter(claims.values()).most_common()[0][1]


def part2(coords, args, p1_state):
    mid = p1_state.value

    safe = set([mid])
    new = set(safe)

    while new:
        next_new = set()
        for x, y in new:
            for nx, ny in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
                if (nx, ny) not in safe and sum(
                    abs(cx - nx) + abs(cy - ny) for cx, cy in coords
                ) < 10_000:
                    safe.add((nx, ny))
                    next_new.add((nx, ny))
        new = next_new

    return len(safe)


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
