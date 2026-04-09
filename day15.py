CAVE = 0
DIRS = 1
ELVES = 2
GOBLINS = 3

TYPE = 0
HP = 1
PSTN = 2


def parse(text):
    lines = text.splitlines()
    width = len(lines[0])
    cave = []
    elves = []
    goblins = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            match char:
                case "E":
                    elf = [char, 200, (x + y * width)]
                    cave.append(elf)
                    elves.append(elf)
                case "G":
                    goblin = [char, 200, (x + y * width)]
                    cave.append(goblin)
                    goblins.append(goblin)
                case _:
                    cave.append(char)
    return cave, (-width, 1, width, -1), elves, goblins


def vprint(*args):
    if 0:
        print(args)


def display(sitrep):
    (cave, (_, _, width, _), _, _) = sitrep
    combatants = []
    for i, item in enumerate(cave):
        if i and (i % width == 0):
            if combatants:
                print("   ", end="")
                print(
                    ", ".join([f"{cmbt[0]}({cmbt[HP]})" for cmbt in combatants]), end=""
                )
                combatants.clear()
            print()
        char = item[0]
        print(char, end="")
        if char != item:
            combatants.append(item)
    print()


def find_open_squares(sitrep, group):
    cave, dirs, *_ = sitrep

    return {
        square
        for _, _, pstn in group
        for dir in dirs
        if cave[square := pstn + dir] == "."
    }


def find_nearest(sitrep, start, group):
    def find(first):
        edge = {first}
        seen = set(edge)
        dist = 0

        while edge:
            dist += 1
            new_edge = set()
            for e in edge:
                if e in group:
                    return dist
                for dir in dirs:
                    if (n := e + dir) not in seen:
                        seen.add(n)
                        if cave[n] == ".":
                            new_edge.add(n)
            edge = new_edge

        return None

    vprint("Finding nearest from start:", start, "to group:", group)

    cave, dirs, *_ = sitrep

    dist_firsts = [
        (dist, first)
        for dir in dirs
        if cave[first := start + dir] == "." and (dist := find(first)) is not None
    ]

    if not dist_firsts:
        return None
    dist_firsts.sort()
    vprint("dist_firsts", dist_firsts)
    return dist_firsts[0][1]


def move(sitrep, combatant, dest):
    cave = sitrep[CAVE]
    source = combatant[PSTN]
    vprint("moving", combatant, "to", dest, (cave[source], cave[dest]))
    cave[dest] = combatant
    cave[source] = "."
    combatant[PSTN] = dest
    vprint("moved", combatant, (cave[source], cave[dest]))


def select_target(sitrep, combatant, targets):
    cave, dirs, *_ = sitrep
    pstn = combatant[PSTN]
    adjacent = [pstn + dir for dir in sitrep[DIRS]]
    in_reach = [target for target in targets if target[PSTN] in adjacent]
    if not in_reach:
        return None
    in_reach.sort(key=lambda targ: (targ[HP], targ[PSTN]))
    return in_reach[0]


def attack_target(sitrep, targets, target):
    vprint("Attacking", target)
    target[HP] -= 3
    if target[HP] <= 0:
        vprint("Killed", target, targets)
        targets.remove(target)
        vprint("Removed", target, targets)
        sitrep[CAVE][target[PSTN]] = "."


def take_turn(sitrep, combatant):
    if combatant[HP] <= 0:
        return
        print("I'M NOT DEAD YET! - OH YES YOU ARE!")

    targets = sitrep[GOBLINS] if combatant[TYPE] == "E" else sitrep[ELVES]

    target = select_target(sitrep, combatant, targets)
    if not target:
        open_squares = set(find_open_squares(sitrep, targets))
        if not open_squares:
            return

        next_step = find_nearest(sitrep, combatant[PSTN], open_squares)
        if not next_step:
            return

        move(sitrep, combatant, next_step)
        target = select_target(sitrep, combatant, targets)

    vprint("Got target:", target)
    if target:
        attack_target(sitrep, targets, target)


def battle(sitrep):
    complete_rounds = 0
    while sitrep[ELVES] and sitrep[GOBLINS]:
        print()
        print(f"After {complete_rounds} Rounds:")
        display(sitrep)

        start_positions = sorted(
            sitrep[ELVES] + sitrep[GOBLINS], key=lambda combatant: combatant[PSTN]
        )
        vprint("start positions:", start_positions)
        for combatant in start_positions:
            if not (sitrep[ELVES] and sitrep[GOBLINS]):
                break
            take_turn(sitrep, combatant)
        else:
            complete_rounds += 1

    print()
    print(f"After {complete_rounds} Rounds:")
    display(sitrep)
    print()

    hp = sum(cmbt[HP] for army in [sitrep[ELVES], sitrep[GOBLINS]] for cmbt in army)
    print(complete_rounds, " * ", hp)
    print()
    return hp * complete_rounds


def part1(sitrep, args, p1_state):
    print(f"\n{sitrep}\n")
    return battle(sitrep)


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
