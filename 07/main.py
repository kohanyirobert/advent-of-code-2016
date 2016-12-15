import re
from sys import stdin


class Seq:

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return '{}{{{}}}'.format(self.__class__.__name__[:3], self.string)

    def __repr__(self):
        return self.__str__()

    def has_abba(self):
        return self.get_abba() != None

    def get_abba(self):
        s = self.string
        l = len(s)
        o = 4
        for i in range(0, l - o + 1):
            p = s[i:i + o]
            if p[0] != p[1] and \
                    p[0] == p[3] and \
                    p[1] == p[2]:
                return p
        return None


class SupSeq(Seq):

    def __init__(self, string):
        super(SupSeq, self).__init__(string)


class HypSeq(Seq):

    def __init__(self, string):
        super(HypSeq, self).__init__(string)


class IPV7Address:

    @classmethod
    def fromstring(cls, string):
        parts = re.split(r'[\[\]]', string)
        sup_seqs = [SupSeq(x) for x in parts[::2]]
        hyp_seqs = [HypSeq(x) for x in parts[1::2]]
        return cls(sup_seqs, hyp_seqs)

    def __init__(self, sup_seqs, hyp_seqs):
        self.sup_seqs = sup_seqs
        self.hyp_seqs = hyp_seqs

    def __str__(self):
        return '{}, {}'.format(self.sup_seqs, self.hyp_seqs)

    def has_tls(self):
        return any([x.has_abba() for x in self.sup_seqs]) and \
            not any([x.has_abba() for x in self.hyp_seqs])


def get_addresses():
    s = stdin.read().strip('\n').split('\n')
    return [IPV7Address.fromstring(x) for x in s]


def main():
    counter = 0
    for address in get_addresses():
        if address.has_tls():
            counter += 1
    print(counter)


main()
