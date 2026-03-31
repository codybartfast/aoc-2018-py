from pathlib import Path
import workshop as ws

YEAR = 2018
BASE = Path(__file__).parent


def read_solvers():
    import runpy

    solvers = []

    for day in range(1, 26):
        input_path = BASE / f"input/{YEAR}/day{day:02}/input.txt"
        solver_path = BASE / f"day{day:02}.py"

        if not (input_path.is_file() and solver_path.is_file()):
            continue

        input = open(input_path).read().strip("\n")
        earn_stars = runpy.run_path(str(solver_path))["earn_stars"]

        solvers.append((input, earn_stars))

    return solvers


def earn_all_stars():
    import time

    h_print = ws.h_print

    solvers = read_solvers()

    start = time.perf_counter()

    for input, earn_stars in solvers:
        earn_stars(text=input)

    stop = time.perf_counter()

    print()
    print()
    h_print()
    h_print(f"Total Time: {ws.friendly_time(stop - start)}")
    h_print()
    print()


if __name__ == "__main__":
    earn_all_stars()
