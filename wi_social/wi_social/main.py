from scipy.sparse import linalg
import numpy as np
import pickle


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

    with open('tmp.txt', 'w+') as f:
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

names = sorted(di.keys())  #[:100]

#names = [1, 2, 3, 4, 5, 6, 7, 8, 9]

matrix = []
for user in names:
    matrix.append([])
    for friend in names:
        if friend in di[user]:
            matrix[-1].append(1)
        else:
            matrix[-1].append(0)


def calc_laplacian(A):
    for i in range(len(A)):
        A[i] = list(map(lambda x: float(-x), A[i]))
        A[i][i] = float(sum(A[i]) * -1)
    return A


print("Created matrix.")
A = matrix
#A = [[0, 1, 1, 0, 0, 0, 0, 0, 0],
#    [1, 0, 1, 0, 0, 0, 0, 0, 0],
#    [1, 1, 0, 1, 1, 0, 0, 0, 0],
#    [0, 0, 1, 0, 1, 1, 1, 0, 0],
#    [0, 0, 1, 1, 0, 1, 1, 0, 0],
#    [0, 0, 0, 1, 1, 0, 1, 1, 0],
#    [0, 0, 0, 1, 1, 1, 0, 1, 0],
#    [0, 0, 0, 0, 0, 1, 1, 0, 1],
#    [0, 0, 0, 0, 0, 0, 0, 1, 0]]
L = calc_laplacian(A)
L = np.array(L)
print("Created A.")


print("Computed eigen-stuff")


def get_eigen_vector(L):
    try:
        with open('eigenvector.pickle', 'rb') as handle:
            ve = pickle.load(handle)
            print('Loaded eigenvector from file')
    except:
        print('Calculating eigenvector - may take a while.')
        va, ve = linalg.eigs(L, k=2, which='SM', v0=np.array([1, ]*len(names)))

        with open('eigenvector.pickle', 'wb') as handle:
            pickle.dump(ve, handle)
    return ve
    

ve = get_eigen_vector(L)

#name_vec_list = ()

#i = 0
#for v in ve:
#    name_vec_list += (v[1].real, names[i]),
#    i += 1

#sorted_name_vec = sorted(name_vec_list, key=lambda tup: tup[0])

#for pair in sorted_name_vec:
#    print("Name: ", pair[1], " - Vec: ", pair[0])

#def find_clusters(snv, diff):
#    curval = snv[0][0]
#    clusters = []
#    clusters.append( () )

#    i = 0
#    for pair in snv:
#        if (curval + diff) < pair[0]:
#            curval = pair[0]
#            i += 1
#            clusters.append( () )

#        clusters[i] += pair,

#    return len(clusters), clusters

#num, clusters = find_clusters(sorted_name_vec, 0.24)

#print("\nClusters: ", num, "\n")

#i = 0
#for cluster in clusters:
#    print("Cluster ", i)
#    i += 1
#    for pair in cluster:
#        print(pair[1], " ", pair[0])
#    print("\n")


#print(L)
#i = 0
#for e in ve:
#    print(str(e) + ' ' + names[i])
#    i += 1





# s = set()
# for k in di.keys():
# s = s.union(set(di[k]))
# s.add(k)
# print(len(s))
# print(len(di))
#
# print(s.difference(set(di.keys())))
