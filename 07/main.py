import re
from sys import stdin


class Seq:

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return '{}{{{}}}'.format(self.__class__.__name__[:3], self.string)

    def __repr__(self):
        return self.__str__()

    def has_xyyx(self):
        return len(self.get_all_xyyx()) != 0

    def get_all_xyyx(self):
        r = []
        s = self.string
        l = len(s)
        o = 4
        for i in range(0, l - o + 1):
            p = s[i:i + o]
            if p[0] != p[1] and \
                    p[0] == p[3] and \
                    p[1] == p[2]:
                r.append(p)
        return r

    def has_xyx(self):
        return len(self.get_all_xyx()) != 0

    def get_all_xyx(self):
        r = []
        s = self.string
        l = len(s)
        o = 3
        for i in range(0, l - o + 1):
            p = s[i:i + o]
            if p[0] != p[1] and p[0] == p[2]:
                r.append(p)
        return r


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
        return any([x.has_xyyx() for x in self.sup_seqs]) and \
            not any([x.has_xyyx() for x in self.hyp_seqs])

    def has_ssl(self):
        sup_aba = [x.get_all_xyx() for x in self.sup_seqs if x.has_xyx()]
        sup_aba = set([x for sublist in sup_aba for x in sublist])
        hyp_bab = [x.get_all_xyx() for x in self.hyp_seqs if x.has_xyx()]
        hyp_bab = set([x for sublist in hyp_bab for x in sublist])
        if len(sup_aba) == 0 or len(hyp_bab) == 0:
            return False
        hyp_aba = [''.join([x[1], x[0], x[1]]) for x in hyp_bab]
        res = len(sup_aba.intersection(hyp_aba)) != 0
        return res


def get_addresses():
    s = stdin.read().strip('\n').split('\n')
    return [IPV7Address.fromstring(x) for x in s]


def main():
    tls_counter = 0
    ssl_counter = 0
    for address in get_addresses():
        if address.has_tls():
            tls_counter += 1
        if address.has_ssl():
            ssl_counter += 1
    print('TLS', tls_counter)
    print('SSL', ssl_counter)


main()
