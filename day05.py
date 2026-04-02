def parse(text):
    return text.encode()

def part1(polymer, args, p1_state):
    print(f"\n{polymer}\n")
    reacted = []
    idx = 0

    while idx < len(polymer):
        reacted.append(polymer[idx])
        idx += 1
        while(reacted and idx < len(polymer) and reacted[-1] ^ polymer[idx] == 32):
            reacted.pop()
            idx += 1

    return len(reacted)


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
