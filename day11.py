BIG_NEG = -(10**18)


def parse(text):
    return int(text)


def calc_grid(gsn):
    grid = [0] * 300 * 300
    for y in range(300):
        for x in range(300):
            pl = ((x + 10) * y + gsn) * (x + 10)
            grid[y * 300 + x] = ((pl % 1000) // 100) - 5
    return grid


def calc_ttls(grid):
    ttls = [0] * 300 * 300
    ttls[0] = grid[0]
    for x in range(1, 300):
        ttls[x] = ttls[x - 1] + grid[x]
    for y in range(300, 300 * 300, 300):
        ttls[y] = ttls[y - 300] + grid[y]
    for y in range(300, 300 * 300, 300):
        for x in range(1, 300):
            i = x + y
            ttls[i] = ttls[i - 1] + ttls[i - 300] - ttls[i - 301] + grid[i]
    return ttls


def best_square_of_size(ttls, size):
    # not covering x = 0 or y = 0

    best_ttl = BIG_NEG
    for y in range(0, 300 - size):
        for x in range(0, 300 - size):
            ttl = (
                ttls[x + size + (y + size) * 300]
                - ttls[x + (y + size) * 300]
                - ttls[x + size + y * 300]
                + ttls[x + y * 300]
            )
            if ttl > best_ttl:
                best_ttl = ttl
                bx, by = x, y

    return best_ttl, (bx + 1, by + 1, size)


def part1(data, args, p1_state):
    grid = calc_grid(data)

    best_start = None
    best_ttl = BIG_NEG
    for y in range(297):
        for x in range(297):
            ttl = sum(
                sum(grid[idx : idx + 3])
                for idx in range(x + y * 300, x + (y + 3) * 300, 300)
            )
            if ttl > best_ttl:
                best_ttl = ttl
                best_start = x, y

    p1_state.value = grid
    print(best_ttl)
    return best_start


def part2(data, args, p1_state):
    grid = p1_state.value
    ttls = calc_ttls(grid)
    best = (BIG_NEG, None)
    for size in range(1, 300):
        size_best = best_square_of_size(ttls, size)
        if size_best[0] > best[0]:
            best = size_best
    return best[1]


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
