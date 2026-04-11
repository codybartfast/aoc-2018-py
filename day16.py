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

    text1, text2 = text.split("\n\n\n\n")
    part1 = list(batched(map(numbers, [ln for ln in text1.splitlines() if ln]), 3))
    part2 = list(map(numbers, text2.splitlines()))

    return part1, part2


def apply(opname, instr, regs):
    _, arg1, arg2, dest = instr

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
    stats = [None] * len(OPNAMES)
    stats_idx = 0
    for opname in OPNAMES:
        stats[stats_idx] = apply(opname, instr, list(before)) == after
        stats_idx += 1
    return stats


def match_ops(samples, stats):
    summary = [[True] * len(OPNAMES)] * len(OPNAMES)
    for sample, stat in zip(samples, stats):
        idx = sample[1][0]
        summary[idx] = [(smry and rslt) for smry, rslt in zip(summary[idx], stat)]
        
    # for x in summary:
    #     print([int(x) for x in x])
        
    code_to_name = {}
    while len(code_to_name) < len(OPNAMES):    
        for code, matches in enumerate(summary):
            if sum(matches) == 1:
                true_idx = matches.index(True)
                name = OPNAMES[true_idx]
                code_to_name[code] = name
                for mtchs in summary:
                    mtchs[true_idx] = False

                # print(code, " => ", name)
                # for x in summary:
                #     print([int(x) for x in x])
                break
        else:
            assert False

    return code_to_name
                

def run(program, code_to_name):
    regs = [0] * 4
    for instr in program:
        regs = apply(code_to_name[instr[0]], instr, regs)
    return regs
    


def part1(data, args, p1_state):
    samples, program = data
    all_stats = [consistent_ops(sample) for sample in samples]
    p1_state.value = all_stats
    return sum(sum(stats) >= 3 for stats in all_stats)


def part2(data, args, p1_state):
    samples, program = data
    all_stats = p1_state.value
    code_to_name = match_ops(samples, all_stats)
    return run(program, code_to_name)[0]


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
