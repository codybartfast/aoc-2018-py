#  2018 Day 16
#  ===========
#
#  Part 1: 592
#  Part 2: 557
#
#  Timings
#  --------------------------------------
#      Parse:     0.002595s  (2.595 ms)
#     Part 1:     0.002043s  (2.043 ms)
#     Part 2:     0.000369s  (369.0 µs)
#    Elapsed:     0.005054s  (5.054 ms)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


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

N_OPS = len(OPNAMES)


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

    return regs


def consistent_ops(sample):
    before, instr, after = sample
    stats = [None] * len(OPNAMES)
    for idx, opname in enumerate(OPNAMES):
        stats[idx] = apply(opname, instr, list(before)) == after
    return stats


def match_ops(samples, stats):
    summary = [[True] * len(OPNAMES)] * len(OPNAMES)
    for (_, (code, *_), _), stat in zip(samples, stats):
        summary[code] = [summary[code][idx] and stat[idx] for idx in range(N_OPS)]

    code_to_name = {}
    for _ in range(N_OPS):
        for code, matches in enumerate(summary):
            if sum(matches) == 1:
                true_idx = matches.index(True)
                name = OPNAMES[true_idx]
                code_to_name[code] = name
                for mtchs in summary:
                    mtchs[true_idx] = False
                break

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
