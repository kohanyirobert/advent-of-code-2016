from sys import stdin


class Movement:

    def __init__(self, name):
        self.name = name
        if self.name == 'U':
            self.direction = (-1, 0)
        elif self.name == 'R':
            self.direction = (0, 1)
        elif self.name == 'D':
            self.direction = (1, 0)
        else:
            self.direction = (0, -1)

    def __str__(self):
        return '{}({:2},{:2})'.format(self.name, self.direction[0], self.direction[1])


class Keypad:

    def __init__(self):
        self.grid = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        self.pushed_keys = []

    def __str__(self):
        s = ''
        for row in self.grid:
            for cell in row:
                s += str(cell)
            s += '\n'
        return s.strip('\n')

    def is_on_keypad(self, x, y):
        return 0 <= x and 0 <= y and x < 3 and y < 3

    def push_key(self, x, y):
        self.pushed_keys.append(str(self.grid[x][y]))


class Finger:

    def __init__(self, keypad):
        self.keypad = keypad
        self.x = 1
        self.y = 1

    def __str__(self):
        return '{},{}'.format(self.x, self.y)

    def move(self, movement):
        x = self.x + movement.direction[0]
        y = self.y + movement.direction[1]
        if self.keypad.is_on_keypad(x, y):
            self.x = x
            self.y = y


def get_finger_path_all_digits():
    l = stdin.read().strip('\n').split('\n')
    return [[Movement(s) for s in p] for p in l]


def main():
    keypad = Keypad()
    print(keypad)
    finger = Finger(keypad)
    all_paths = get_finger_path_all_digits()
    for path in all_paths:
        for movement in path:
            finger.move(movement)
            print(movement, finger, keypad.grid[finger.x][finger.y])
        keypad.push_key(finger.x, finger.y)
        print('PUSH', keypad.pushed_keys[-1])
    print(''.join(keypad.pushed_keys))

if __name__ == '__main__':
    main()
