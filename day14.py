#  2018 Day 14
#  ===========
#
#  Part 1: 6126491027
#  Part 2: 20191615
#
#  Timings
#  --------------------------------------
#      Parse:     0.000000s  (0.291 µs)
#     Part 1:     0.021608s  (21.61 ms)
#     Part 2:     1.471188s  (1.471 s)
#    Elapsed:     1.492864s  (1.493 s)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


# Since relatively straightforward did lots of micro optimisations so not pretty


def parse(text):
    return text


def part1(text, args, p1_state):
    n_recipe = int(text)
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1

    reqd = n_recipe + 10

    while reqd:
        sum = (r1 := recipes[elf1]) + (r2 := recipes[elf2])
        if sum >= 10:
            recipes.append(1)
        recipes.append(sum % 10)
        elf1 = (elf1 + 1 + r1) % len(recipes)
        elf2 = (elf2 + 1 + r2) % len(recipes)
        reqd -= 1

    return "".join(str(rcp) for rcp in recipes[n_recipe : n_recipe + 10])


def part2(text, args, p1_state):

    target = [int(c) for c in text]
    [t1, t2, t3, t4, t5, t6] = target
    assert t6 == 1  # almost certainly always the case.
    assert t5 != 1  # if true don't need to check second of two appends
    t_len = len(target)

    recipes = [3, 7]
    rep_len = 2
    elf1 = 0
    elf2 = 1

    while True:
        sum = (rcp1 := recipes[elf1]) + (rcp2 := recipes[elf2])
        if sum >= 10:
            recipes.append(1)
            if (
                recipes[-2] == t5
                and recipes[-3] == t4
                and recipes[-4] == t3
                and recipes[-5] == t2
                and recipes[-6] == t1
            ):
                break
            recipes.append(sum % 10)
            rep_len += 2
        else:
            recipes.append(d := sum % 10)
            rep_len += 1
            if (
                d == 1
                and recipes[-2] == t5
                and recipes[-3] == t4
                and recipes[-4] == t3
                and recipes[-5] == t2
                and recipes[-6] == t1
            ):
                break
        elf1 = (elf1 + 1 + rcp1) % rep_len
        elf2 = (elf2 + 1 + rcp2) % rep_len

    return len(recipes) - t_len


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
