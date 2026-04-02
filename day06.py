from collections import Counter


def parse(text):

    def parse_line(line):
        parts = line.split(", ")
        return int(parts[0]), int(parts[1])

    lines = text.splitlines()
    return [parse_line(line) for line in lines]


def part1(coords, args, p1_state):
    min_x = min(x for x, y in coords)
    max_x = max(x for x, y in coords)
    min_y = min(y for x, y in coords)
    max_y = max(y for x, y in coords)

    p1_state.value = (min_x + max_x) // 2, (min_y + max_y) // 2

    def to_infinity(coord):
        x, y = coord
        return x == min_x or x == max_x or y == min_y or y == max_y

    areas = {}
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            dists = [(abs(x - cx) + abs(y - cy), (cx, cy)) for cx, cy in coords]
            dists.sort()
            if dists[0][0] != dists[1][0]:
                areas.setdefault(dists[0][1], []).append((x, y))

    finite = [
        area for area in areas.values() if not any(to_infinity(coord) for coord in area)
    ]

    return max(len(area) for area in finite)


def part2(coords, args, p1_state):
    mid = p1_state.value

    safe = set([mid])
    new = set(safe)

    while new:
        new = set(
            (nx, ny)
            for x, y in new
            for nx, ny in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
            if (nx, ny) not in safe
            and sum(abs(cx - nx) + abs(cy - ny) for cx, cy in coords) < 10_000
        )
        safe.update(new)

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
