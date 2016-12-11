from sys import stdin


def reverse_frequency_map(frequency_map):
    result = {}
    for k, v in frequency_map.items():
        if v not in result:
            result[v] = []
        result[v].append(k)
        result[v].sort()
    return result


def reverse_frequency_maps(frequency_maps):
    return [reverse_frequency_map(m) for m in frequency_maps]


def get_frequency_maps(messages):
    frequency_maps = None
    for message in messages:
        size = len(message)
        if frequency_maps is None:
            frequency_maps = [{} for _ in range(size)]
        for i in range(size):
            char = message[i]
            frequency_map = frequency_maps[i]
            if char not in frequency_map:
                frequency_map[char] = 1
            else:
                frequency_map[char] += 1
    return frequency_maps


def get_most_frequent_char(reverse_frequency_map):
    highest_count = max(reverse_frequency_map)
    most_frequent_chars = reverse_frequency_map[highest_count]
    most_frequent_char = most_frequent_chars[0]
    return most_frequent_char


def correct(messages):
    m = reverse_frequency_maps(get_frequency_maps(messages))
    return ''.join([get_most_frequent_char(r) for r in m])


def main():
    messages = [l.strip('\n') for l in stdin.readlines()]
    print(correct(messages))


main()
