#  2018 Day 13
#  ===========
#
#  Part 1: 43,111
#  Part 2: 44,56
#
#  Timings
#  --------------------------------------
#      Parse:     0.000868s  (868.0 µs)
#     Part 1:     0.005971s  (5.971 ms)
#     Part 2:     0.000000s  (0.334 µs)
#    Elapsed:     0.006872s  (6.872 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


PSTN = 0


def parse(text):

    lines = text.splitlines()
    width = len(lines[0])

    carts = []
    track = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            match char:
                case "^":
                    carts.append(([x + y * width, 0, 0]))
                    track.append("|")
                case ">":
                    carts.append(([x + y * width, 1, 0]))
                    track.append("-")
                case "v":
                    carts.append(([x + y * width, 2, 0]))
                    track.append("|")
                case "<":
                    carts.append(([x + y * width, 3, 0]))
                    track.append("-")
                case _:
                    track.append(char)

    return width, "".join(track), carts


def part1(survey, args, p1_state):
    width, track, carts = survey
    DIRS = [-width, 1, width, -1]

    pstns = set([cart[0] for cart in carts])
    first_collision = None
    wreck = None
    while len(carts) > 1:
        next_carts = []

        for pstn, dir, choice in carts:
            if pstn == wreck:
                wreck = None
                continue
            pstns.remove(pstn)

            match track[pstn]:
                case "|" | "-":
                    pass
                case "/":
                    dir = (dir + (1 if dir in [0, 2] else -1)) % 4
                case "\\":
                    dir = (dir + (1 if dir in [1, 3] else -1)) % 4
                case "+":
                    dir = (dir + choice - 1) % 4
                    choice = (choice + 1) % 3
                case _:
                    assert False
            pstn += DIRS[dir]

            if pstn not in pstns:
                pstns.add(pstn)
                next_carts.append((pstn, dir, choice))
            else:
                if not first_collision:
                    first_collision = pstn
                pstns.remove(pstn)
                n_next = len(next_carts)
                next_carts = [cart for cart in next_carts if cart[PSTN] != pstn]
                if len(next_carts) == n_next:
                    wreck = pstn
        carts = next_carts

    last_cart = carts[0][PSTN]
    p1_state.value = f"{last_cart % width},{last_cart // width}"

    return f"{first_collision % width},{first_collision // width}"


def part2(survey, args, p1_state):
    return p1_state.value


# Runner
################################################################################


def collect_stars(text=None, filepath=None, extra_args=None):
    import workshop

    if not text and filepath:
        text = open(filepath).read()
    workshop.get_cracking(text, parse, part1, part2, extra_args)


if __name__ == "__main__":
    import sys
    import workshop

    file = sys.argv[1] if len(sys.argv) > 1 else None
    filepath = workshop.get_filepath(file)
    if filepath:
        extra_args = sys.argv[2:]
        collect_stars(filepath=filepath, extra_args=extra_args)
