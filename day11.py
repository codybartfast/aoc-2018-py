#  2018 Day 11
#  ===========
#
#  Part 1: 245,14
#  Part 2: 235,206,13
#
#  Timings
#  --------------------------------------
#      Parse:     0.000001s  (0.666 µs)
#     Part 1:     0.016937s  (16.94 ms)
#     Part 2:     0.561674s  (561.7 ms)
#    Elapsed:     0.578650s  (578.7 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


# I originally completed this in 2018 in the naive way of adding all the
# individual values, I was impressed then by a much faster solution which I
# reproduce here.  It calculates to total for each rectangle (0, 0) to (x, y)
# for all x, y.  You then only need to add/sub four numbers to get the total of
# any rectangle.


def parse(text):
    return int(text)


def calc_grid(grid_serial_number):
    grid = [0] * 300 * 300
    for y in range(300):
        for x in range(300):
            pl = ((x + 10) * y + grid_serial_number) * (x + 10)
            grid[y * 300 + x] = ((pl % 1000) // 100) - 5
    return grid


def calc_totals(grid):
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
    # I only added the handling of x or y = 0 after completing the solution.  I
    # doubt they're needed, but then I'm not sure they're correct either.

    size_300 = size * 300
    size_301 = size_300 + size

    # x = 0, y = 0
    bx, by = -1, -1
    best_ttl = ttls[size_301]

    # x > 0, y = 0
    for x in range(0, 300 - size):
        ttl = ttls[x + size] - ttls[x]
        if ttl > best_ttl:
            best_ttl = ttl
            bx, by = x, 0

    # x = 0, 0 < y
    for y in range(0, 300 - size):
        offset = (size - 1) + y * 300
        ttl = ttls[offset + size_300] - ttls[offset]
        if ttl > best_ttl:
            best_ttl = ttl
            bx, by = x, 0

    # 0 < x, 0 < y
    for y in range(0, 300 - size):
        for x in range(0, 300 - size):
            offset = x + y * 300
            ttl = (
                ttls[offset + size_301]
                - ttls[offset + size_300]
                - ttls[offset + size]
                + ttls[offset]
            )
            if ttl > best_ttl:
                best_ttl = ttl
                bx, by = x, y

    return best_ttl, (bx + 1, by + 1, size)


def part1(grid_serial_number, _, p1_state):
    grid = calc_grid(grid_serial_number)
    ttls = calc_totals(grid)
    p1_state.value = ttls

    _, (x, y, _) = best_square_of_size(ttls, 3)
    return ",".join(map(str, (x, y)))


def part2(_, __, p1_state):
    ttls = p1_state.value
    best = (0, ())
    for size in range(1, 300):
        size_best = best_square_of_size(ttls, size)
        if size_best[0] > best[0]:
            best = size_best

    return ",".join(map(str, best[1]))


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
