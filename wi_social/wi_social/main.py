from scipy.sparse import linalg
import numpy as np
import pickle
import sentiment

class Person:

    def __init__(self, name, friends, review):
        self.name = name
        self.friends = friends
        self.review = review

        self.score = -1
        self.buy = False
        self.cluster = -1



def foo():
    users = []
    res = []
    with open('friendships.reviews.txt', 'r') as f:
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
    persondict = {}
    with open('tmp.txt', 'r') as f:
        cur_user = ''
        friends = []
        review = ''

        for line in f.readlines():
            if line.count('user:'):
                cur_user = line[6:-1]
            elif line.count('friends:'):
                friends = line[9:-1].split()
            elif line.count('summary:'):
                if line[9:-1] == '*':
                    review = False
                else:
                    review = line[9:-1] + '. '
            elif line.count('review:'):
                if review:
                    review += line[8:-1]
            persondict[cur_user] = Person(cur_user, friends, review)

    return persondict


foo()
p_dict = bar()
#names = [1, 2, 3, 4, 5, 6, 7, 8, 9]

names = sorted(p_dict.keys())#[:10]

matrix = []
for user in names:
    matrix.append([])
    for friend in names:
        if friend in p_dict[user].friends:
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
    va, ve = linalg.eigsh(L, k=2, which='LM', sigma=1)
    #try:
    #    with open('eigenvector.pickle', 'rb') as handle:
    #        ve = pickle.load(handle)
    #        print('Loaded eigenvector from file')
    #except:
    #    print('Calculating eigenvector - may take a while.')
    #    va, ve = linalg.eigsh(L, k=2, which='LM', sigma=0.001)

    #    with open('eigenvector.pickle', 'wb') as handle:
    #        pickle.dump(ve, handle)
    return ve
    

ve = get_eigen_vector(L)
print('Done!')

name_vec_list = ()

i = 0
for v in ve:
    name_vec_list += (v[1].real, names[i]),
    i += 1

sorted_name_vec = sorted(name_vec_list, key=lambda tup: tup[0])

print(sorted_name_vec[0])
print(sorted_name_vec[-1])

#for pair in sorted_name_vec:
#    print("Name: ", pair[1], " - Vec: ", pair[0])


def cluster(snv):
    diffs = []
    for i in range(len(snv)-1):
        diffs.append((snv[i+1][0]-snv[i][0],
                      (snv[i+1][0]-snv[i][0])/snv[i+1][0]*100,
                      i,
                      i+1,
                      snv[i],
                      snv[i+1]))
    return diffs


def find_clusters(snv):
    c = 0
    for i in range(len(snv)-1):
        if (snv[i+1][0]-snv[i][0])/snv[i+1][0]*100 > 50 and (snv[i+1][0]-snv[i][0])/snv[i+1][0]*100 < 100:
            c += 1
        p_dict[snv[i][1]].cluster = c
    p_dict[snv[-1][1]].cluster = c
    print("Clusters:", c)


#for val in [0.01, 0.009, 0.008, 0.007, 0.006, 0.005, 0.004, 0.003, 0.001, 0.0009]:
#    num, clusters = find_clusters(sorted_name_vec, val)
#    print("Clusters: ", num, " Diff value: ", val, "\n")

find_clusters(sorted_name_vec)



for person in p_dict:
    if p_dict[person].review:
       p_dict[person].score = sentiment.scoreTest(sentiment.Review(3, p_dict[person].review))

avg_score = []
for person in p_dict:
    if not p_dict[person].review:
        for friend in p_dict[person].friends:
            if not friend in p_dict:
                continue

            significance = 1
            if p_dict[friend].score != -1:
                if p_dict[friend].name == 'kyle':
                    significance *= 10
                if p_dict[friend].cluster != p_dict[person].cluster:
                    significance *= 10
                for x in range(0, significance):
                    avg_score.append(p_dict[friend].score)
        if sum(avg_score)/len(avg_score) >= 4.8:
            p_dict[person].buy = True

for person in p_dict:
    if p_dict[person].buy:
        print(person, "bought things.")




diff = cluster(sorted_name_vec)
print("sorted by abs")
for e in list(sorted(diff, key=lambda tup: 0-tup[0]))[:10]:
    print(e)
print("sorted by %")
for e in list(sorted(diff, key=lambda tup: 0-tup[1]))[:10]:
    print(e)

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
#    print(str(e) + ' ' + str(names[i]))
#    i += 1





# s = set()
# for k in di.keys():
# s = s.union(set(di[k]))
# s.add(k)
# print(len(s))
# print(len(di))
#
# print(s.difference(set(di.keys())))
