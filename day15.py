#  2018 Day 15
#  ===========
#
#  Part 1: 188576
#  Part 2: 57112
#
#  Timings
#  --------------------------------------
#      Parse:     0.000057s  (56.62 µs)
#     Part 1:     0.053395s  (53.39 ms)
#     Part 2:     0.356191s  (356.2 ms)
#    Elapsed:     0.409682s  (409.7 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


from dataclasses import dataclass


@dataclass
class Combatant:
    type: str
    hp: int
    pstn: int

    def copy(self):
        return Combatant(self.type, self.hp, self.pstn)


@dataclass
class Sitrep:
    cave: list[str | Combatant]
    dirs: tuple
    elves: list[Combatant]
    goblins: list[Combatant]
    elf_attack_power: int

    def total_hitpoint(self):
        return sum(cmbt.hp for army in [self.elves, self.goblins] for cmbt in army)


def parse(text):
    lines = text.splitlines()
    width = len(lines[0])
    dirs = -width, 1, width, -1
    cave = []
    elves = []
    goblins = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            match char:
                case "E":
                    elf = Combatant(char, 200, (x + y * width))
                    cave.append(elf)
                    elves.append(elf)
                case "G":
                    goblin = Combatant(char, 200, (x + y * width))
                    cave.append(goblin)
                    goblins.append(goblin)
                case _:
                    cave.append(char)

    return lambda: Sitrep(
        list(cave),
        dirs,
        [elf.copy() for elf in elves],
        [gbl.copy() for gbl in goblins],
        3,
    )


def display_cave(sitrep: Sitrep):
    width = sitrep.dirs[2]
    combatants = []
    for i, item in enumerate(sitrep.cave):
        if i and (i % width == 0):
            if combatants:
                print("   ", end="")
                print(
                    ", ".join([f"{cmbt.type}({cmbt.hp})" for cmbt in combatants]),
                    end="",
                )
                combatants.clear()
            print()
        char = item.type if isinstance(item, Combatant) else item
        print(char, end="")
        if char != item:
            combatants.append(item)
    print()


def find_open_squares(sitrep: Sitrep, group):

    return {
        square
        for combatant in group
        for dir in sitrep.dirs
        if sitrep.cave[square := combatant.pstn + dir] == "."
    }


def find_nearest(sitrep: Sitrep, first, group):
    edge = {first}
    seen = set(edge)
    dist = 0

    while edge:
        dist += 1
        new_edge = set()
        for e in edge:
            if e in group:
                return dist
            for dir in sitrep.dirs:
                if (n := e + dir) not in seen:
                    seen.add(n)
                    if sitrep.cave[n] == ".":
                        new_edge.add(n)
        edge = new_edge

    return None


def find_next_move(sitrep: Sitrep, start, group):

    dist_next = [
        (dist, first)
        for dir in sitrep.dirs
        if sitrep.cave[first := start + dir] == "."
        and (dist := find_nearest(sitrep, first, group)) is not None
    ]

    if not dist_next:
        return None
    dist_next.sort()
    return dist_next[0][1]


def move(sitrep: Sitrep, combatant, dest):
    cave = sitrep.cave
    source = combatant.pstn
    cave[dest] = combatant
    cave[source] = "."
    combatant.pstn = dest


def select_target(sitrep: Sitrep, combatant, targets):
    pstn = combatant.pstn
    adjacent = [pstn + dir for dir in sitrep.dirs]
    in_reach = [target for target in targets if target.pstn in adjacent]
    if not in_reach:
        return None
    in_reach.sort(key=lambda targ: (targ.hp, targ.pstn))
    return in_reach[0]


def attack_target(sitrep: Sitrep, targets, target):
    attack_power = 3 if target.type == "E" else sitrep.elf_attack_power
    target.hp -= attack_power
    if target.hp <= 0:
        targets.remove(target)
        sitrep.cave[target.pstn] = "."


def take_turn(sitrep: Sitrep, combatant):
    if combatant.hp <= 0:
        return
        print("I'M NOT DEAD YET! - OH YES YOU ARE!")

    targets = sitrep.goblins if combatant.type == "E" else sitrep.elves

    target = select_target(sitrep, combatant, targets)
    if not target:
        open_squares = set(find_open_squares(sitrep, targets))
        if not open_squares:
            return

        next_step = find_next_move(sitrep, combatant.pstn, open_squares)
        if not next_step:
            return

        move(sitrep, combatant, next_step)
        target = select_target(sitrep, combatant, targets)

    if target:
        attack_target(sitrep, targets, target)


def battle(sitrep: Sitrep):
    complete_rounds = 0
    while sitrep.elves and sitrep.goblins:
        start_positions = sorted(
            sitrep.elves + sitrep.goblins, key=lambda combatant: combatant.pstn
        )
        for combatant in start_positions:
            if not (sitrep.elves and sitrep.goblins):
                break
            take_turn(sitrep, combatant)
        else:
            complete_rounds += 1

    return complete_rounds


def part1(get_sitrep, args, p1_state):
    sitrep: Sitrep = get_sitrep()
    complete_rounds = battle(sitrep)
    hp = sitrep.total_hitpoint()
    return hp * complete_rounds


def part2(get_sitrep, args, p1_state):
    sitrep: Sitrep = get_sitrep()
    elf_ep = 4
    sitrep.elf_attack_power = elf_ep
    n_elves = len(sitrep.elves)

    while (rounds := battle(sitrep)) and len(sitrep.elves) < n_elves:
        elf_ep += 1
        sitrep = get_sitrep()
        sitrep.elf_attack_power += elf_ep

    hp = sitrep.total_hitpoint()
    return hp * rounds


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
