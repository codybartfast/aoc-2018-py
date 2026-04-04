def parse(text):
    import re

    re_digits = re.compile(r"-?\d+")

    def numbers(txt):
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


def sky(coords):
    (x_min, y_min), (x_max, y_max) = corners(coords)
    sky = [['.'] * (x_max - x_min + 1) for _ in range(y_min, y_max + 1)]
    for x, y in coords:
        sky[y - y_min][x - x_min] = "#"
    return "\n".join("".join(row) for row in sky)
    

def part1(lights, args, p1_state):
    vectors = [light[1] for light in lights]
    (_, dy_min), (_, dy_max) = corners(vectors)
    falling = [light for light in lights if light[1][1] == dy_min][0]
    rising = [light for light in lights if light[1][1] == dy_max][0]
    closing_x_velocity = dy_max - dy_min
    x_dist = falling[0][1] - rising[0][1]
    time = x_dist // closing_x_velocity
    time += 1 # because
    coords = advance(lights, time)
    p1_state.value = time
    return "\n" + sky(coords)

def part2(data, args, p1_state):
    return p1_state.value


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
