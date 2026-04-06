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


def advance(DIRS, track, cart, _width):
    pstn, dir, choice = cart

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
            assert False, (pstn % 108, pstn // 108, track[pstn])
    pstn += DIRS[dir]
    return pstn, dir, choice


def part1(survey, args, p1_state):
    # print(f"\n{survey}\n")
    width, track, carts = survey
    DIRS = [-width, 1, width, -1]

    pstns = [cart[0] for cart in carts]
    collision = None
    while not collision:
        next_carts = []
        for cart in carts:
            pstn = cart[0]
            cart = advance(DIRS, track, cart, width)
            pstns.remove(pstn)
            pstn = cart[0]
            if pstn in pstns:
                collision = pstn
                break
            pstns.append(pstn)
            next_carts.append(cart)
        carts = next_carts

    return f"{collision % width},{collision // width}"


def part2(survey, args, p1_state):
    width, track, carts = survey
    DIRS = [-width, 1, width, -1]

    pstns = [cart[0] for cart in carts]
    crashed = None
    while len(carts) > 1:
        next_carts = []
        for cart in carts:
            if cart == crashed:
                crashed = None
                continue
            pstn = cart[0]
            cart = advance(DIRS, track, cart, width)
            pstns.remove(pstn)
            pstn = cart[0]
            if pstn in pstns:
                pstns.remove(pstn)
                n_next = len(next_carts)
                next_carts = [cart for cart in next_carts if cart[0] != pstn]
                if len(next_carts) == n_next:
                    crashed = [cart for cart in carts if cart[0] == pstn][0]
            else:
                pstns.append(pstn)
                next_carts.append(cart)
        carts = next_carts

    last_collision = carts[0][0]
    return f"{last_collision % width},{last_collision // width}"


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
