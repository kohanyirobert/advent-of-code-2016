from sys import stdin


class Step:

    @classmethod
    def fromraw_step(cls, raw_step):
        turn = raw_step[0]
        distance = int(raw_step[1:])
        return cls(turn, distance)

    def __init__(self, turn, distance):
        self.turn = turn
        self.distance = distance

    def __str__(self):
        return '{}{}'.format(self.turn, self.distance)


class Direction:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        if self == NORTH:
            return 'N'
        elif self == EAST:
            return 'E'
        elif self == SOUTH:
            return 'S'
        else:
            return 'W'


class Me:

    def __init__(self):
        self.direction = NORTH
        self.x = 0
        self.y = 0

    def __str__(self):
        return '{:3},{:3} {}'.format(self.x, self.y, self.direction)

    def _turn(self, step):
        index = DIRECTIONS.index(self.direction)
        offset = 1 if step.turn == 'R' else -1
        index = (index + offset) % len(DIRECTIONS)
        self.direction = DIRECTIONS[index]

    def _move(self, step):
        self.x += self.direction.x * step.distance
        self.y += self.direction.y * step.distance

    def follow(self, step):
        self._turn(step)
        self._move(step)

    def distance(self):
        return abs(self.x) + abs(self.y)


NORTH = Direction(0, 1)
EAST = Direction(1, 0)
SOUTH = Direction(0, -1)
WEST = Direction(-1, 0)

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]


def get_raw_steps():
    return stdin.read().strip('\n').split(', ')


def get_steps(raw_steps):
    return [Step.fromraw_step(raw_step) for raw_step in raw_steps]


def follow_steps(me, steps):
    print(me, 'START')
    for step in steps:
        me.follow(step)
        print(me, step)
    print(me, 'STOP')


def main():
    me = Me()
    raw_steps = get_raw_steps()
    steps = get_steps(raw_steps)
    follow_steps(me, steps)
    print(me.distance())


if __name__ == '__main__':
    main()
