from sys import stdin


table = []
for line in stdin.readlines():
    row = [int(s) for s in line.split()]
    table.append(row)

count = 0
for i in range(0, len(table), 3):
    groupped_rows = []
    for j in range(3):
        groupped_rows.append(table[i + j])
    for k in range(3):
        sides = []
        for j in range(3):
            sides.append(groupped_rows[j][k])
        sides.sort()
        if sum(sides[0:2]) > sides[2]:
            count += 1
print(count)
