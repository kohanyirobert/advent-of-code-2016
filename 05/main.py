from sys import stdin
from hashlib import md5

door_id = stdin.read().strip('\n')

password_positions = {}
i = 0
while len(password_positions) != 8:
    unhashed = door_id + str(i)
    hashed = md5(unhashed.encode()).hexdigest()
    if hashed[:5] == '00000':
        j = hashed[5]
        if '0' <= j < '8' and j not in password_positions:
            k = hashed[6]
            password_positions[j] = k
    i += 1
password = sorted(password_positions.items(), key=lambda x: x[0])
print(''.join([x[1] for x in password]))
