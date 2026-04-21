#  2018 Day 19
#  ===========
#
#  Part 1: 2223
#  Part 2: 24117312
#
#  Timings
#  --------------------------------------
#      Parse:     0.000012s  (11.96 µs)
#     Part 1:     0.000047s  (47.04 µs)
#     Part 2:     0.002634s  (2.634 ms)
#    Elapsed:     0.002728s  (2.728 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


def parse(text):

    def parse_line(line):
        parts = line.split()
        return parts[0], int(parts[1]), int(parts[2]), int(parts[3])

    lines = text.splitlines()
    return int(lines[0][-1]), [parse_line(line) for line in lines[1:]]


def boot(reg_zero=0):
    regs = [0] * 6
    regs[0] = reg_zero
    return regs


def run(pcr, prog, regs):
    pc = 0

    while 0 <= pc < len(prog):
        regs[pcr] = pc
        opname, arg1, arg2, dest = prog[pc]

        match opname:
            case "addr":
                regs[dest] = regs[arg1] + regs[arg2]
            case "addi":
                regs[dest] = regs[arg1] + arg2
            case "mulr":
                regs[dest] = regs[arg1] * regs[arg2]
            case "muli":
                regs[dest] = regs[arg1] * arg2
            case "banr":
                regs[dest] = regs[arg1] & regs[arg2]
            case "bani":
                regs[dest] = regs[arg1] & arg2
            case "borr":
                regs[dest] = regs[arg1] | regs[arg2]
            case "bori":
                regs[dest] = regs[arg1] | arg2
            case "setr":
                regs[dest] = regs[arg1]
            case "seti":
                regs[dest] = arg1
            case "gtir":
                regs[dest] = arg1 > regs[arg2]
            case "gtri":
                regs[dest] = regs[arg1] > arg2
            case "gtrr":
                regs[dest] = regs[arg1] > regs[arg2]
            case "eqir":
                regs[dest] = arg1 == regs[arg2]
            case "eqri":
                regs[dest] = regs[arg1] == arg2
            case "eqrr":
                regs[dest] = regs[arg1] == regs[arg2]

            # new instructions
            case "modr":
                regs[dest] = regs[arg1] % regs[arg2]
            case "divr":
                regs[dest] = regs[arg1] // regs[arg2]

        pc = regs[pcr]
        pc += 1

    return regs


def refactor(prog):
    # Get r2 mod r1
    prog[2] = ("modr", 2, 1, 4)
    prog[3] = ("eqri", 4, 0, 4)
    prog[4] = ("addr", 4, 3, 3)
    # if non-zero jump to finally
    prog[5] = ("addi", 3, 5, 3)
    # if zero add r1 to r0
    prog[6] = ("addr", 1, 0, 0)
    # ... and add co-factor
    prog[7] = ("divr", 2, 1, 4)
    prog[8] = ("addr", 4, 0, 0)
    prog[9] = ("addi", 3, 1, 3)

    # finally ...
    prog[11] = ("addi", 1, 1, 1)
    # Check if r1 * r1 > r2
    prog[12] = ("mulr", 1, 1, 4)
    prog[13] = ("gtrr", 4, 2, 4)
    # ...


def part1(data, args, p1_state):
    pcr, prog = data

    refactor(prog)

    regs = boot()
    run(pcr, prog, regs)
    return regs[0]


def part2(data, args, p1_state):
    pcr, prog = data

    refactor(prog)

    regs = boot(1)
    run(pcr, prog, regs)
    return regs[0]


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
