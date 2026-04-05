from datetime import datetime
from pathlib import Path
import platform
import re
import sys
import time

YEAR = "2018"


# pot mods:
#   -


def get_day():
    filename = Path(sys._getframe(2).f_code.co_filename).name

    day_match = re.search(r"day(\d\d)", filename)
    if not day_match:
        raise RuntimeError(f"Couldn't get day from filename: {filename}")
    return day_match.group(1)


def get_filepath(file):
    if not file:
        file = "input"
    canonical = (
        Path(__file__).resolve().parent
        / "input"
        / YEAR
        / f"day{get_day()}"
        / (file + ".txt")
    )
    if canonical.is_file():
        return canonical
    other = Path(file)
    if other.is_file():
        return other
    print()
    print("Couldn't find input file.")
    print(f"Tried: '{canonical}'")
    print(f"  and: '{other.resolve()}'")
    return None


def h_print(*args):
    print("# ", *args)


class State:
    def __init__(self):
        self.ans1 = None
        self.value = None


def get_cracking(text, parse, part1, part2, extra_args):

    state = State()

    pc_start = time.perf_counter()
    day = get_day()

    title = f"{YEAR} Day {day.lstrip('0')}"

    print("\n")
    h_print(title)
    h_print("=" * len(title))
    h_print()

    pc_parse_before = time.perf_counter()
    data = parse(text)
    pc_parse_after = time.perf_counter()

    pc_part1_before = time.perf_counter()
    ans1 = part1(data, extra_args, state)
    pc_part1_after = time.perf_counter()
    h_print(f"Part 1: {ans1}")

    state.ans1 = ans1

    pc_part2_before = time.perf_counter()
    ans2 = part2(data, extra_args, state)
    pc_part2_after = time.perf_counter()
    h_print(f"Part 2: {ans2}")

    pc_stop = time.perf_counter()

    parse_time = pc_parse_after - pc_parse_before
    part1_time = pc_part1_after - pc_part1_before
    part2_time = pc_part2_after - pc_part2_before
    elapsed = pc_stop - pc_start

    timings = []
    timings.append(f"    Parse: {parse_time:12.6f}s  ({friendly_time(parse_time)})")
    timings.append(f"   Part 1: {part1_time:12.6f}s  ({friendly_time(part1_time)})")
    timings.append(f"   Part 2: {part2_time:12.6f}s  ({friendly_time(part2_time)})")
    timings.append(f"  Elapsed: {elapsed:12.6f}s  ({friendly_time(elapsed)})")

    bar_width = max(len(timing) for timing in timings) + 2
    h_print()
    h_print("Timings")
    h_print("-" * bar_width)
    for timing in timings:
        h_print(timing)
    h_print("-" * bar_width)
    h_print()
    h_print(f"   Date:  {datetime.now().strftime('%B %Y')}")
    h_print(f"Machine:  {machine()}")
    h_print(f" Python:  {platform.python_version()}")
    print(" ")


def friendly_time(span):
    def format(span):
        places = 3
        if span >= 1000:
            assert False
        elif span >= 100:
            places = 1
        elif span >= 10:
            places = 2
        return f"{span:.{places}f}"

    if span < 0.001:
        span *= 1_000_000
        return format(span) + " µs"
    if span < 1:
        span *= 1_000
        return format(span) + " ms"
    if span < 60:
        return format(span) + " s"
    if span < 600:
        m = int(span // 60)
        s = span - m * 60
        return f"{m}m {s:0.1f}s"
    if span < 600:
        m = int(span // 60)
        s = span - m * 60
        return f"{m}m {s:0.1f}s"
    time_str = ""
    if span >= 3600:
        h = int(span // 3600)
        time_str += f"{h}h "
        span -= 3600 * h
    m = int(span // 60)
    span -= m * 60
    time_str += f"{m}m {span:.0f}s"
    return time_str


def machine():
    fp = machine_fingerprint()
    return {"fffcc23": "MacBook M4"}.get(fp, fp)


def machine_fingerprint():
    from hashlib import md5
    from os import cpu_count
    from platform import node, machine

    fp = f"on the back in Nordic Elvish:{node()}:{machine()}:{cpu_count()}"
    return md5(fp.encode()).hexdigest()[:7]


def read_raster(raster: list[str]):
    BIG = 10**18

    alphabet_6 = "ABCEFGHIJKLOPRSUYZ"
    glyphabet_6 = [
        ".##..###...##..####.####..##..#..#..###...##.#..#.#.....##..###..###...###.#..#.#...#####.",
        "#..#.#..#.#..#.#....#....#..#.#..#...#.....#.#.#..#....#..#.#..#.#..#.#....#..#.#...#...#.",
        "#..#.###..#....###..###..#....####...#.....#.##...#....#..#.#..#.#..#.#....#..#..#.#...#..",
        "####.#..#.#....#....#....#.##.#..#...#.....#.#.#..#....#..#.###..###...##..#..#...#...#...",
        "#..#.#..#.#..#.#....#....#..#.#..#...#..#..#.#.#..#....#..#.#....#.#.....#.#..#...#..#....",
        "#..#.###...##..####.#.....###.#..#..###..##..#..#.####..##..#....#..#.###...##....#..####.",
    ]

    alphabet_10 = "ABCEFGHJKLNPRXZ"
    glyphabet_10 = [
        "..##....#####....####...######..######...####...#....#.....###..#....#..#.......#....#..#####...#####...#....#..######..",
        ".#..#...#....#..#....#..#.......#.......#....#..#....#......#...#...#...#.......##...#..#....#..#....#..#....#.......#..",
        "#....#..#....#..#.......#.......#.......#.......#....#......#...#..#....#.......##...#..#....#..#....#...#..#........#..",
        "#....#..#....#..#.......#.......#.......#.......#....#......#...#.#.....#.......#.#..#..#....#..#....#...#..#.......#...",
        "#....#..#####...#.......#####...#####...#.......######......#...##......#.......#.#..#..#####...#####.....##.......#....",
        "######..#....#..#.......#.......#.......#..###..#....#......#...##......#.......#..#.#..#.......#..#......##......#.....",
        "#....#..#....#..#.......#.......#.......#....#..#....#......#...#.#.....#.......#..#.#..#.......#...#....#..#....#......",
        "#....#..#....#..#.......#.......#.......#....#..#....#..#...#...#..#....#.......#...##..#.......#...#....#..#...#.......",
        "#....#..#....#..#....#..#.......#.......#...##..#....#..#...#...#...#...#.......#...##..#.......#....#..#....#..#.......",
        "#....#..#####....####...######..#........###.#..#....#...###....#....#..######..#....#..#.......#....#..#....#..######..",
    ]

    def normalise(raster):
        # Trims empty space all around, checks dimensions, adds back trailing
        # space after last char
        
        raster = [line for line in raster if "#" in line]
        height = len(raster)
        if height not in [6, 10]:
            print("\n" + "\n".join(raster) + "\n")
            raise RuntimeError(f"Unexpected number of lines: {height} (expect 6 or 10)")

        x_min = BIG
        x_max = -BIG
        for line in raster:
            x_min = min(x_min, line.find("#"))
            x_max = max(x_max, line.rfind("#"))

        width = x_max - x_min + 1
        suffix = "." if height == 6 else ".."
        raster = [line[x_min : x_min + width] + suffix for line in raster]
        width += len(suffix)
        if height == 6 and width % 5:
            print("\n" + "\n".join(raster) + "\n")
            raise RuntimeError(f"Unexpected width: {width} (expect multiple of 5)")
        elif height == 10 and width % 8:
            print("\n" + "\n".join(raster) + "\n")
            raise RuntimeError(f"Unexpected width: {width} (expect multiple of 8)")

        return raster

    def split_glyphs(glyphs, width):
        tp_glyphs = list(zip(*glyphs))
        sep_glyphs = []
        while tp_glyphs:
            tp_glyph, tp_glyphs = tp_glyphs[:width], tp_glyphs[width:]
            sep_glyphs.append("\n".join("".join(row) for row in zip(*tp_glyph)))
        return sep_glyphs

    def read(alphabet, glyphabet, raster, char_width):
        glyph_dict = dict(zip(split_glyphs(glyphabet, char_width), alphabet))
        return "".join(glyph_dict[glyph] for glyph in split_glyphs(raster, char_width))

    raster = normalise(raster)
    match len(raster):
        case 6:
            return read(alphabet_6, glyphabet_6, raster, 5)
        case 10:
            return read(alphabet_10, glyphabet_10, raster, 8)
        case _:
            assert False # normalise() should prevent this
