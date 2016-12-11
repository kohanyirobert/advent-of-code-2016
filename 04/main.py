from sys import stdin


class Instruction:

    @classmethod
    def fromstring(cls, instruction):
        last_dash_index = instruction.rfind('-')
        first_bracket_index = instruction.find('[')
        encrypted_name = instruction[:last_dash_index]
        encrypted_name = encrypted_name.replace('-', '')
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
            if not char in char_map:
                char_map[char] = 1
            char_map[char] += 1
        return char_map

    def _get_count_map(self):
        count_map = {}
        char_map = self._get_char_map()
        for k, v in char_map.items():
            if not v in count_map:
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

    def is_real(self):
        count_ordered_chars = self._get_count_ordered_chars()
        return self.checksum == ''.join(count_ordered_chars[:5])


def get_instructions():
    l = stdin.read().strip('\n').split('\n')
    return [Instruction.fromstring(s) for s in l]


def main():
    sector_id_sum = 0
    for instruction in get_instructions():
        is_real = instruction.is_real()
        print('REAL' if is_real else 'FAKE', instruction)
        if is_real:
            sector_id_sum += instruction.sector_id
    print(sector_id_sum)

main()
