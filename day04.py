#  2018 Day 4
#  ==========
#
#  Part 1: 115167
#  Part 2: 32070
#
#  Timings
#  --------------------------------------
#      Parse:     0.000306s  (306.3 µs)
#     Part 1:     0.000080s  (79.63 µs)
#     Part 2:     0.000097s  (97.08 µs)
#    Elapsed:     0.000520s  (519.8 µs)
#  --------------------------------------
#
#     Date:  April 2026
#  Machine:  MacBook M4
#   Python:  3.14.3


def parse(text):  # and sort
    def parse_line(line):
        parts = line.split()
        return int(parts[1][3:5]), parts[3]

    lines = sorted(text.splitlines())
    return [parse_line(line) for line in lines]


def naps_by_guard(observations):
    nap_db = {}

    for i, (minute, event) in enumerate(observations):
        match event[0]:
            case "#":  #  #<guard-id>
                guard = event
                time_asleep, nap_spans = nap_db.get(guard, (0, []))
            case "a":  # falls [a]sleep
                nap_start = minute
            case "u":  # wakes [u]p
                time_asleep += minute - nap_start
                nap_spans.append((nap_start, minute))
                nap_db[guard] = time_asleep, nap_spans
            case _:
                assert False, event

    return nap_db


def sleepy_minute(spans):
    hour = [0] * 60
    for start, end in spans:
        for min in range(start, end):
            hour[min] += 1

    max_naps = max(hour)
    return hour.index(max_naps), max_naps


def part1(observations, args, p1_state):
    nap_db = naps_by_guard(observations)

    guard, (time_asleep, nap_spans) = max(nap_db.items(), key=lambda kvp: kvp[1][0])

    p1_state.value = nap_db
    nappy_minute, nap_count = sleepy_minute(nap_spans)
    return int(guard[1:]) * nappy_minute


def part2(_, __, p1_state):
    nap_db = p1_state.value

    strat2 = [(guard, sleepy_minute(spans)) for (guard, (_, spans)) in nap_db.items()]
    guard, (sleep_time, _) = max(strat2, key=lambda info: info[1][1])

    return int(guard[1:]) * sleep_time


# Runner
################################################################################


def collect_stars(text=None, filepath=None, extra_args=None):
    import workshop as ws

    if not text and filepath:
        text = open(filepath).read().strip()
    ws.get_cracking(text, parse, part1, part2, extra_args)


if __name__ == "__main__":
    import sys
    import workshop as ws

    file = sys.argv[1] if len(sys.argv) > 1 else None
    filepath = ws.get_filepath(file)
    if filepath:
        extra_args = sys.argv[2:]
        collect_stars(filepath=filepath, extra_args=extra_args)
