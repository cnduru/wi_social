from happyfuntokenizing import Tokenizer
from progressTrack import Progress
from math import log

num_rev = {}
voc = {}
voclength = 0

class Review:
    t = Tokenizer()

    def __init__(self, text, score=0):
        self.score = score
        self.text = self._negate(self.t.tokenize(text))
        
    def _negate(self, text):
        negatelist = ["never", "no", "nothing", "nowhere", 
                      "noone", "none", "not", "havent", "hasnt", 
                      "hadnt", "cant", "couldnt", "shouldnt",
                      "wont", "wouldnt", "dont", "doesnt", 
                      "didnt", "isnt", "arent", "aint"]
        punctlist = [".", ":", ";", "!", "?"]
        new_text = []

        neg = False
        for word in text:
            if word in punctlist:
                neg = False
            if neg:
                word = word + "_NEG"
            if word in negatelist:
                neg = True

            new_text.append(word)
        return new_text

def count_sentiments(reviews):
    global num_rev, voc, voclength

    for x in range(1,6):
        num_rev[x] = 0
        voc[x] = {}

    for review in reviews:
        num_rev[review.score] += 1

        for word in review.text:
            if word in voc[review.score]:
                voc[review.score][word] += 1
            else:
                voc[review.score][word] = 1

    fullvoc = set()

    for x in range(1,6):
        fullvoc = fullvoc.union(set(voc[x].keys()))

    voclength = len(fullvoc)

    #return num_rev, voc, voclength

def parse_reviews(start_line, end_line):
    score = 0
    text = ""
    reviews = []
    cur_line = 0

    # clear screen
    print('                    ', end='\r')

    with open('SentimentTrainingData.txt', 'r') as f:
        #update end_line
        if end_line > len(f.readlines()):
            end_line = len(f.readlines())

        # start at line start_line
        f.seek(start_line)
        p = Progress(end_line, "Parsing reviews")
        for line in f.readlines():

            cur_line += 1
            p.percent(cur_line)
            # make sure we start the right place
            if cur_line < start_line:
                continue

            if line[:14] == "review/score: ":
                score = int(line[14])
            if line[:16] == "review/summary: ":
                text += line[16:] + '.'
            if line[:13] == "review/text: ":
                text += line[13:]

                #Store and reset
                reviews.append(Review(text, score))
                text = ""

                # end read at line end_line
                if cur_line >= end_line:
                    break
    return reviews

def prob_sentiment(sentiment):
    global num_rev
    n = sum(num_rev.values())
    nc = num_rev[sentiment]
    return (nc + 1)/(n + 5)

def prob_word_in_sentiment(word, sentiment):
    global num_rev, voc, voclength
    nc = num_rev[sentiment]
    if word in voc[sentiment]:
        nxc = voc[sentiment][word]
    else:
        nxc = 0

    return (nxc + 1)/(nc + voclength)


def log_score (review, sentiment):
    pxc = 0

    for word in review.text:
        pxc += log(prob_word_in_sentiment(word, sentiment))

    return log(prob_sentiment(sentiment)) + pxc

def scoreTest(review):

    lst = []

    for n in range(1,6):
        this_val = log_score(review, n)
        lst.append(this_val)

    return lst.index(max(lst)) + 1

revs = parse_reviews(1, 1000000)
count_sentiments(revs)

to_be_reviewed = parse_reviews(2000000, 2005000)



#test_revs = [Review("The WORST coffee !. The worst!!! it is just plan awful bitter and strong and you cannot taste the Hazel Nut flavor at all!!!!!  Do not buy this product save your money!!!!!")]

#print(score(test_revs[0], num_rev, voc))

total_hits = 0
cnt = 0
pos_hits = 0
neg_hits = 0
neu_hits = 0
tot_pos = 0
tot_neg = 0
tot_neu = 0
scores = []
total_reviews = len(to_be_reviewed)

# clear screen
print("\r\n")

p = Progress(total_reviews, "Computing scores")

for rev in to_be_reviewed:
    score = scoreTest(rev)

    if score not in scores:
        scores.append(score)

    if rev.score in [4, 5]:
        tot_pos +=1
    elif rev.score == 3:
        tot_neu +=1
    elif rev.score in [1,2]:
        tot_neg +=1

    if (score in [4,5]) and (rev.score in [4, 5]):
        total_hits += 1
        pos_hits +=1

    elif score == 3 and rev.score == 3:
        total_hits += 1
        neu_hits +=1

    elif (score in [1, 2]) and (rev.score in [1, 2]):
        total_hits += 1
        neg_hits += 1

    cnt += 1
    p.percent(cnt)

print("Scores given: " + str(scores))
print("Hit rate: ", (total_hits/total_reviews)*100, "%")
print("Pos: ", pos_hits, "/", tot_pos, " (", (pos_hits/tot_pos*100), "%)")
print("Neg: ", neg_hits, "/", tot_neg, " (", (neg_hits/tot_neg*100), "%)")
print("Neu: ", neu_hits, "/", tot_neu, " (", (neu_hits/tot_neu*100), "%)")