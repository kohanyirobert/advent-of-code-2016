from sys import stdin


class Text:

    def __init__(self, string):
        self.string = string


class UnmarkedText(Text):

    def __len__(self):
        return len(self.string)


class MarkedText(Text):

    def __init__(self, string, size, times):
        super(MarkedText, self).__init__(string)
        self.size = size
        self.times = times

    def __len__(self):
        return len(Compressed(self.string)) * self.times


class Compressed:

    def __init__(self, string):
        self.string = string

    def __iter__(self):
        s = self.string
        while True:
            start = s.find('(')
            if start == -1:
                yield UnmarkedText(s)
                break
            elif start > 0:
                yield UnmarkedText(s[:start])
                s = s[start:]
            else:
                stop = s.find(')', start)
                size, times = [int(x) for x in s[start + 1:stop].split('x')]
                yield MarkedText(s[stop + 1:stop + size + 1], size, times)
                s = s[stop + size + 1:]

    def __len__(self):
        return sum([len(x) for x in self])


def get_compressed():
    return stdin.read().strip()


def main():
    print(len(Compressed(get_compressed())))

main()
