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
    t_len = len(target)

    recipes = [3, 7]
    elf1 = 0
    elf2 = 1

    while True:
        sum = (r1 := recipes[elf1]) + (r2 := recipes[elf2])
        if sum >= 10:
            recipes.append(1)
            if recipes[-t_len:] == target:
                break
        recipes.append(sum % 10)
        if recipes[-t_len:] == target:
            break
        elf1 = (elf1 + 1 + r1) % len(recipes)
        elf2 = (elf2 + 1 + r2) % len(recipes)

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
