class Marble:
    def __init__(self, value, prev=None):
        self.value = value
        if prev:
            next = prev.next
            self.prev = prev
            self.next = next
            prev.next = self
            next.prev = self
        else:
            self.prev = None
            self.next = None


def parse(text):
    import re

    re_digits = re.compile(r"-?\d+")

    def numbers(txt):
        return [int(t) for t in re_digits.findall(txt)]

    return numbers(text)


def play_game(n_players, last):
    scores = [0] * n_players
    current = Marble(0)
    current.next = current
    current.prev = current

    player = 0
    marble = 0
    while marble < last:
        marble += 1
        player = (player + 1) % n_players

        if marble % 23 or not marble:
            current = current.next
            current = Marble(marble, current)
        else:
            for _ in range(7):
                current = current.prev
            scores[player] += marble + current.value
            prev = current.prev
            next = current.next
            prev.next = next
            next.prev = prev
            current = next

    return scores


def part1(game, args, p1_state):
    n_players, last = game
    return max(play_game(n_players, last))


def part2(game, args, p1_state):
    n_players, last = game
    return max(play_game(n_players, last * 100))


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
