import re


def parse(text):
    re_digits = re.compile(r"-?\d+")

    def parse_line(line):
        return int(line)

    lines = text.splitlines()
    return [parse_line(line) for line in lines]


def part1(data, args, p1_state):
    return sum(data)


def part2(data, args, p1_state):
    freq = 0
    seen = set()

    idx = 0
    while freq not in seen:
        seen.add(freq)
        freq += data[idx]
        idx = (idx + 1) % len(data)
    return freq


# Runner
################################################################################


def earn_stars(text=None, filepath=None, extra_args=None):
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
        earn_stars(filepath=filepath, extra_args=extra_args)
