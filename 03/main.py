from sys import stdin

count = 0
for line in stdin.readlines():
    sides = [int(s) for s in line.split()]
    sides.sort()
    if sum(sides[0:2]) > sides[2]:
        count += 1
print(count)
