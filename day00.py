import re

def parse(text):
    re_digits = re.compile(r"-?\d+")

    def parse_line(line):
        parts = line.split()
        return [part for part in parts]

    lines = text.splitlines()
    return [parse_line(line) for line in lines]


def part1(data, args, p1_state):
    print(f"\n{data}\n")
    return "ans1"


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
