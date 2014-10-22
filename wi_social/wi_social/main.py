from scipy import linalg
import numpy as np

def foo():
    users = []
    res = []
    with open('friendships.txt', 'r') as f:
        for line in f.readlines():
            if line.count('user:') and len(line.split()) > 2:
                users.append(line[6:-1])
        f.seek(0)
        for line in f.readlines():
            l = line
            for user in users:
                l = l.replace(' ' + user, ' ' + user.replace(" ", "_"))
            res.append(l)

    with open('tmp.txtt', 'w+') as f:
        f.write(''.join(res))


def bar():
    """ Hej """
    d = {}
    with open('tmp.txt', 'r') as f:
        cur_user = ''
        for line in f.readlines():
            if line.count('user:'):
                cur_user = line[6:-1]
            elif line.count('friends:'):
                d[cur_user] = line[9:-1].split()

    return d

foo()
di = bar()

names = sorted(di.keys())

matrix = []
for user in names:
    matrix.append([])
    for friend in names:
        if friend in di[user]:
            matrix[-1].append(1)
        else:
            matrix[-1].append(0)

print("Created matrix.")
A = np.array(matrix)
print("Created A.")
la, v = linalg.eig(A)
print("Computed eigen-stuff")
print(la)
# s = set()
# for k in di.keys():
#     s = s.union(set(di[k]))
#     s.add(k)
# print(len(s))
# print(len(di))
#
# print(s.difference(set(di.keys())))
