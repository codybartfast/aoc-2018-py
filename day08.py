class Reader:
    def __init__(self, items):
        self.items = items
        self.idx = 0
        self.remaining = len(items)

    def read(self):
        return self.read_n(1)[0]

    def read_n(self, n):
        assert n <= self.remaining
        rslt = self.items[self.idx : self.idx + n]
        self.idx += n
        self.remaining -= n
        return rslt


class Node:
    def __init__(self, reader):
        n_children = reader.read()
        n_meta = reader.read()
        self.children = [Node(reader) for _ in range(n_children)]
        self.metadata = reader.read_n(n_meta)

    def check_one(self):
        return sum(self.metadata) + sum(node.check_one() for node in self.children)


    def check_two(self):
        if self.children:
            return sum(self.children[i - 1].check_two() for i in self.metadata if 0 < i <= len(self.children))
        else:
            return sum(self.metadata)


def parse(text):
    return list(map(int, text.split()))


def part1(licence, args, p1_state):
    reader = Reader(licence)
    root = Node(reader)
    p1_state.value = root
    return root.check_one()


def part2(data, args, p1_state):
    root = p1_state.value
    return root.check_two()


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
