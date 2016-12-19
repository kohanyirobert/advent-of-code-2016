from sys import stdin


class Screen:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]

    def __str__(self):
        return '\n'.join([''.join(_) for _ in self.grid])

    def __repr__(self):
        return self.__str__()

    def get_lit_count(self):
        return len([c for r in self.grid for c in r if c == '#'])


class Cmd:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.__str__()


class RectCmd(Cmd):

    @classmethod
    def fromstring(cls, string):
        args = string.split('x')
        width = int(args[0])
        height = int(args[1])
        return cls(width, height)

    def __init__(self, width, height):
        super(RectCmd, self).__init__('rect')
        self.width = width
        self.height = height

    def __str__(self):
        return '{}({},{})'.format(self.name, self.width, self.height)

    def apply_to(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                screen.grid[i][j] = '#'


class RotCmd(Cmd):

    def __init__(self, orientation, selector, shift_width):
        super(RotCmd, self).__init__('rotate')
        self.orientation = orientation
        self.selector = selector
        self.shift_width = shift_width

    def __str__(self):
        return '{}({},{},{})'.format(self.name, self.orientation, self.selector, self.shift_width)


class RowRotCmd(RotCmd):

    def __init__(self, selector, shift_width):
        super(RowRotCmd, self).__init__('row', selector, shift_width)

    def apply_to(self, screen):
        row = screen.grid[self.selector]
        for _ in range(self.shift_width):
            row.insert(0, row.pop())


class ColRotCmd(RotCmd):

    def __init__(self, selector, shift_width):
        super(ColRotCmd, self).__init__('column', selector, shift_width)

    def apply_to(self, screen):
        l = len(screen.grid)
        for _ in range(self.shift_width):
            for i in range(l):
                row = screen.grid[i]
                cell = row.pop(self.selector)
                next_i = (i + 1) % l
                next_row = screen.grid[next_i]
                offset = 0 if next_i == 0 else 1
                next_row.insert(self.selector + offset, cell)


class Cmds:

    @classmethod
    def fromstring(_, string):
        parts = string.split()
        command = parts[0]
        if command == 'rect':
            return RectCmd.fromstring(parts[1])
        elif command == 'rotate':
            orientation = parts[1]
            selector = int(parts[2].split('=')[1])
            shift_width = int(parts[4])
            if orientation == 'column':
                return ColRotCmd(selector, shift_width)
            elif orientation == 'row':
                return RowRotCmd(selector, shift_width)
        raise ValueError


def get_commands():
    return [Cmds.fromstring(s) for s in stdin.read().strip().split('\n')]


def main():
    screen = Screen(6, 50)
    for cmd in get_commands():
        cmd.apply_to(screen)
    print(screen)
    print(screen.get_lit_count())

main()
