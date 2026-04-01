import re
from collections import Counter

def parse(text): # and sort
    re_digits = re.compile(r"-?\d+")

    def parse_line(line):
        parts = line.split()
        return int(parts[1][3:5]), parts[3]

    lines = text.splitlines()
    lines.sort()
    return [parse_line(line) for line in lines]

def sleepy_minute(spans):
    hour = [0] * 60
    for start, end in spans:
        for min in range(start, end):
            hour[min] += 1

    return hour.index(max(hour))

def part1(data, args, p1_state):
    guard = None
    duration = None
    spans = None
    db = {}
    sleep_start = None
    for i, (minute, event) in enumerate(data):
        match event[0]:
            case "#":
                guard = event
                duration, spans = db.get(guard, (0, []))
            case "a":
                sleep_start = minute
            case "u":
                assert spans is not None
                duration += (minute - sleep_start)
                spans.append((sleep_start, minute))
                db[guard] = duration, spans
            case _:
                assert False, event
            
    sleepy = max(db.items(), key=lambda kvp: kvp[1][0])
                    
    return int(sleepy[0][1:]) * sleepy_minute(sleepy[1][1])


def part2(data, args, p1_state):
    return "ans2"


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
