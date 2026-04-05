def parse(text):
    return int(text)


def calc_grid(gsn):
    grid = [0] * 300 * 300
    for y in range(300):
        for x in range(300):
            pl = ((x + 10) * y + gsn) * (x + 10)
            grid[y * 300 + x] = ((pl % 1000) // 100) - 5
    return grid


def part1(data, args, p1_state):
    grid = calc_grid(data)

    best_start = None
    best_ttl = -(10 * 18)
    for y in range(297):
        for x in range(297):
            ttl = sum(
                sum(grid[idx : idx + 3])
                for idx in range(x + y * 300, x + (y + 3) * 300, 300)
            )
            if ttl > best_ttl:
                best_ttl = ttl
                best_start = x, y

    return best_start


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
