from sys import stdin
from hashlib import md5

door_id = stdin.read().strip('\n')

password = []
i = 0
while len(password) != 8:
    unhashed = door_id + str(i)
    hashed = md5(unhashed.encode()).hexdigest()
    if hashed[:5] == '00000':
        password.append(hashed[5])
    i += 1
print(''.join(password))
