#  2018 Day 10
#  ===========
#
#  Part 1: BXJXJAEX
#  Part 2: None
#
#  Timings
#  --------------------------------------
#      Parse:     0.000400s  (399.5 µs)
#     Part 1:     0.000231s  (230.5 µs)
#     Part 2:     0.000000s  (0.250 µs)
#    Elapsed:     0.000664s  (663.6 µs)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


import workshop as ws


def parse(text):

    def numbers(txt):
        import re

        re_digits = re.compile(r"-?\d+")
        return [int(t) for t in re_digits.findall(txt)]

    def parse_line(line):
        nums = numbers(line)
        return (nums[0], nums[1]), (nums[2], nums[3])

    return [parse_line(line) for line in text.splitlines()]


def advance(lights, sec):
    return [((x + dx * sec), (y + dy * sec)) for (x, y), (dx, dy) in lights]


def corners(coords):
    x_max = max(coord[0] for coord in coords)
    x_min = min(coord[0] for coord in coords)
    y_max = max(coord[1] for coord in coords)
    y_min = min(coord[1] for coord in coords)
    return (x_min, y_min), (x_max, y_max)


def size(coord):
    (x_min, y_min), (x_max, y_max) = corners(coord)
    return (x_max - x_min) * (y_max - y_min)


def to_grid(coords):
    (x_min, y_min), (x_max, y_max) = corners(coords)
    sky = [["."] * (x_max - x_min + 1) for _ in range(y_min, y_max + 1)]
    for x, y in coords:
        sky[y - y_min][x - x_min] = "#"
    return ["".join(row) for row in sky]


def part1(lights, args, p1_state):

    vectors = [light[1] for light in lights]
    (_, dy_min), (_, dy_max) = corners(vectors)
    falling = next(light for light in lights if light[1][1] == dy_min)
    rising = next(light for light in lights if light[1][1] == dy_max)
    closing_y_velocity = dy_max - dy_min
    y_dist = falling[0][1] - rising[0][1]

    time = y_dist // closing_y_velocity
    coords = advance(lights, time)
    while size(next_coords := advance(lights, time + 1)) < size(coords):
        time += 1
        coords = next_coords

    p1_state.value = time
    return ws.read_raster(to_grid(coords))


def part2(data, args, p1_state):
    return p1_state.value


# Runner
################################################################################


def collect_stars(text=None, filepath=None, extra_args=None):
    if not text and filepath:
        text = open(filepath).read().strip()
    ws.get_cracking(text, parse, part1, part2, extra_args)


if __name__ == "__main__":
    import sys

    file = sys.argv[1] if len(sys.argv) > 1 else None
    filepath = ws.get_filepath(file)
    if filepath:
        extra_args = sys.argv[2:]
        collect_stars(filepath=filepath, extra_args=extra_args)
