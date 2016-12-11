from sys import stdin
from string import ascii_lowercase


ALPHABET_SIZE = len(ascii_lowercase)


class Instruction:

    @classmethod
    def fromstring(cls, instruction):
        last_dash_index = instruction.rfind('-')
        first_bracket_index = instruction.find('[')
        encrypted_name = instruction[:last_dash_index]
        sector_id = int(instruction[last_dash_index + 1:first_bracket_index])
        checksum = instruction[first_bracket_index + 1:-1]
        return cls(encrypted_name, sector_id, checksum)

    def __init__(self, encrypted_name, sector_id, checksum):
        self.encrypted_name = encrypted_name
        self.sector_id = sector_id
        self.checksum = checksum

    def __str__(self):
        return '{:3}-{:5} {}'.format(self.sector_id, self.checksum, self.encrypted_name)

    def _get_char_map(self):
        char_map = {}
        for char in self.encrypted_name:
            if char == '-':
                continue
            if char not in char_map:
                char_map[char] = 1
            char_map[char] += 1
        return char_map

    def _get_count_map(self):
        count_map = {}
        char_map = self._get_char_map()
        for k, v in char_map.items():
            if v not in count_map:
                count_map[v] = []
            count_map[v].append(k)
            count_map[v].sort()
        return count_map

    def _get_count_ordered_chars(self):
        count_map = self._get_count_map()
        count_keys = list(count_map.keys())
        count_keys.sort()
        count_keys.reverse()
        count_ordered_chars = []
        for k in count_keys:
            chars = count_map[k]
            count_ordered_chars.extend(chars)
        return count_ordered_chars

    def _decipher_char(self, char):
        if char == '-':
            return ' '
        char_index = ascii_lowercase.find(char)
        index_offset = self.sector_id % ALPHABET_SIZE
        new_char_index = (char_index + index_offset) % ALPHABET_SIZE
        return ascii_lowercase[new_char_index]

    def is_real(self):
        count_ordered_chars = self._get_count_ordered_chars()
        return self.checksum == ''.join(count_ordered_chars[:5])

    def decipher_name(self):
        return ''.join([self._decipher_char(c) for c in self.encrypted_name])


def get_instructions():
    l = stdin.read().strip('\n').split('\n')
    return [Instruction.fromstring(s) for s in l]


def main():
    sector_id_sum = 0
    northpole_sector_id = None
    for instruction in get_instructions():
        is_real = instruction.is_real()
        if is_real:
            deciphered_name = instruction.decipher_name()
            print('REAL', instruction, instruction.decipher_name())
            sector_id_sum += instruction.sector_id
            if deciphered_name == 'northpole object storage':
                northpole_sector_id = instruction.sector_id
        else:
            print('FAKE', instruction)
    print('SECTOR ID SUM', sector_id_sum)
    print('NORTHPOLE SECTOR ID', northpole_sector_id)

main()
