from collections import Counter

def parse(text):
    def parse_line(line):
        parts = line.split()
        return [part for part in parts]

    lines = text.splitlines()
    return [line for line in lines]


def part1(data, args, p1_state):
    n_two = 0
    n_three = 0
    for id in data:
        counts = Counter(id)
        n_two += 2 in counts.values()
        n_three += 3 in counts.values()
    return n_two * n_three


def part2(data, args, p1_state):
    return "ans2"


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
