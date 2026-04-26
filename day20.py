BIG = 10**18


def parse(text):
    return text


def display(project):
    print()

    x_min = BIG
    x_max = -BIG
    y_min = BIG
    y_max = -BIG

    for x, y in project:
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y

    for y in range(y_min - 1, y_max + 2):
        for x in range(x_min - 1, x_max + 2):
            char = project.get((x, y), "#")
            print(char if type(char) is str else ".", end="")
        print()

    print()


def expand(regex, idx, end, heads, project):
    while (idx := idx + 1) < end:
        match regex[idx]:
            case "N":
                heads = [
                    ((x, y - 2), dist + 1)
                    for (x, y), dist in heads
                    if (x, y - 2) not in project
                ]
                for (x, y), dist in heads:
                    project[x, y + 1] = "-"
                    project[x, y] = min(dist, project.get((x, y), BIG))
            case "E":
                heads = [
                    ((x + 2, y), dist + 1)
                    for (x, y), dist in heads
                    if (x + 2, y) not in project
                ]
                for (x, y), dist in heads:
                    project[x - 1, y] = "|"
                    project[x, y] = min(dist, project.get((x, y), BIG))
            case "S":
                heads = [
                    ((x, y + 2), dist + 1)
                    for (x, y), dist in heads
                    if (x, y + 2) not in project
                ]
                for (x, y), dist in heads:
                    project[x, y - 1] = "-"
                    project[x, y] = min(dist, project.get((x, y), BIG))
            case "W":
                heads = [
                    ((x - 2, y), dist + 1)
                    for (x, y), dist in heads
                    if (x - 2, y) not in project
                ]
                for (x, y), dist in heads:
                    project[x + 1, y] = "|"
                    project[x, y] = min(dist, project.get((x, y), BIG))
            case "(":
                start = idx
                bars = []
                depth = 0
                while depth >= 0:
                    idx += 1
                    match regex[idx]:
                        case "(":
                            depth += 1
                        case "|":
                            if depth == 0:
                                bars.append(idx)
                        case ")":
                            if depth == 0:
                                bars.append(idx)
                            depth -= 1
                        case _:
                            continue

                new_heads = []
                for bar in bars:
                    new_heads.extend(expand(regex, start, bar, list(heads), project))
                    start = bar
                return expand(regex, idx, end, new_heads, project)
            case "$":
                pass
            case _:
                assert False, f"{idx}:'{regex[idx]}'"

    return heads


def part1(regex, args, p1_state):
    project = {(0, 0): 0}
    expand(regex, 0, len(regex), [((0, 0), 0)], project)
    display(project)
    dists = [dist for dist in project.values() if type(dist) is int]
    return max(dists)


def part2(data, args, p1_state):
    return "ans2"


# Runner
################################################################################


def collect_stars(text=None, filepath=None, extra_args=None):
    import workshop

    if not text and filepath:
        text = open(filepath).read().strip()
    workshop.get_cracking(text, parse, part1, part2, extra_args)


if __name__ == "__main__":
    import sys
    import workshop

    file = sys.argv[1] if len(sys.argv) > 1 else None
    filepath = workshop.get_filepath(file)
    if filepath:
        extra_args = sys.argv[2:]
        collect_stars(filepath=filepath, extra_args=extra_args)
