OPNAMES = [
    "addr",
    "addi",
    "mulr",
    "muli",
    "banr",
    "bani",
    "borr",
    "bori",
    "setr",
    "seti",
    "gtir",
    "gtri",
    "gtrr",
    "eqir",
    "eqri",
    "eqrr",
]


def parse(text):
    from itertools import batched
    import re

    re_digits = re.compile(r"-?\d+")

    def numbers(txt):
        return [int(t) for t in re_digits.findall(txt)]

    text1, text2 = text.split("\n\n\n")
    part1 = list(batched(map(numbers, [ln for ln in text1.splitlines() if ln]), 3))
    part2 = list(map(numbers, text2.splitlines()))

    return part1, part2


def apply(opname, instr, in_regs):
    _, arg1, arg2, dest = instr
    regs = list(in_regs)

    if opname[0] in ["g", "e"]:
        op_class = opname[:-2]
        match opname[-2:]:
            case "ir":
                val1, val2 = arg1, regs[arg2]
            case "ri":
                val1, val2 = regs[arg1], arg2
            case "rr":
                val1, val2 = regs[arg1], regs[arg2]
            case _:
                assert False
    else:
        op_class = opname[:-1]
        if op_class == "set":
            match opname[-1:]:
                case "r":
                    val1, val2 = regs[arg1], None
                case "i":
                    val1, val2 = arg1, None
                case _:
                    assert False
        else:
            match opname[-1:]:
                case "r":
                    val1, val2 = regs[arg1], regs[arg2]
                case "i":
                    val1, val2 = regs[arg1], arg2
                case _:
                    assert False

    match op_class:
        case "add":
            regs[dest] = val1 + val2
        case "mul":
            regs[dest] = val1 * val2
        case "ban":
            regs[dest] = val1 & val2
        case "bor":
            regs[dest] = val1 | val2
        case "set":
            regs[dest] = val1
        case "gt":
            regs[dest] = int(val1 > val2)
        case "eq":
            regs[dest] = int(val1 == val2)
        case _:
            assert False, op_class

    return regs

    


def consistent_ops(sample):
    before, instr, after = sample
    consistent = set()
    for opname in OPNAMES:
        if apply(opname, instr, before) == after:
            consistent.add(opname)
    return consistent



def part1(data, args, p1_state):
    samples, program = data
    # print(f"\n{samples}\n")

    return sum(1 for sample in samples if  len(consistent_ops(sample)) >= 3)


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
