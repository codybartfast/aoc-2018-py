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

    # blah = 0 if regs[0] else 1001

    while 0 <= pc < len(prog):
        regs[pcr] = pc
        opname, arg1, arg2, dest = prog[pc]

        # print(pc, prog[pc], regs)

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
                # print(pc, regs[arg1], regs[arg2], regs[arg1] > regs[arg2])
                regs[dest] = regs[arg1] > regs[arg2]
            case "eqir":
                regs[dest] = arg1 == regs[arg2]
            case "eqri":
                regs[dest] = regs[arg1] == arg2
            case "eqrr":
                regs[dest] = regs[arg1] == regs[arg2]

            case "modr":
                # print(regs[arg1], regs[arg2], regs[arg1] % regs[arg2])
                regs[dest] = regs[arg1] % regs[arg2]

        pc = regs[pcr]
        pc += 1

        # blah += 1
        # if blah == 1000:
        #     print(regs)
        #     exit()

    return regs


def part1(data, args, p1_state):
    pcr, prog = data
    regs = boot()
    run(pcr, prog, regs)
    return regs[0]


def part2(data, args, p1_state):
    pcr, prog = data

    prog[2] = ("modr", 2, 1, 4)
    prog[3] = ("gtri", 4, 0, 4)
    prog[4] = ("addr", 4, 3, 3)
    prog[5] = ("addr", 1, 0, 0)
    prog[6] = ("addi", 3, 5, 3)

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
