from sys import stdin


class Marker:

    @classmethod
    def fromstring(cls, string):
        start = string.find('(')
        if start == -1:
            return None
        stop = string.find(')', start)
        length, times = [int(_) for _ in string[start + 1:stop].split('x')]
        return cls(string, start, stop, length, times)

    def __init__(self, string, start, stop, length, times):
        self.string = string
        self.marker_start = start
        self.marker_stop = stop
        self.marker_length = length
        self.marker_times = times
        self.start = self.marker_stop + 1
        self.stop = self.marker_stop + self.marker_length + 1

    def __str__(self):
        s = ', '.join(['{}={}'] * 6)
        return s.format(
            'marker_start', self.marker_start,
            'marker_stop', self.marker_stop,
            'marker_length', self.marker_length,
            'marker_times', self.marker_times,
            'start', self.start,
            'stop', self.stop,
        )

    def decompress(self):
        decompressed = self.string[:self.marker_start]
        decompressed += self.marker_times * self.string[self.start:self.stop]
        compressed = self.string[self.stop:]
        return decompressed, compressed


class Decompression:

    def __init__(self, compressed):
        self.decompressed = ''
        self.compressed = compressed

    def decompress(self):
        while True:
            marker = Marker.fromstring(self.compressed)
            if marker == None:
                break
            decompressed, compressed = marker.decompress()
            self.decompressed += decompressed
            self.compressed = compressed


def get_compressed():
    return stdin.read().strip()


def main():
    decompression = Decompression(get_compressed())
    decompression.decompress()
    print(len(decompression.decompressed))

main()
