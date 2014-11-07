from happyfuntokenizing import Tokenizer
from math import log

vocabulary = set()
num_rev_1 = 0
num_rev_2 = 0
num_rev_3 = 0
num_rev_4 = 0
num_rev_5 = 0
voc_1 = {}
voc_2 = {}
voc_3 = {}
voc_4 = {}
voc_5 = {}

class Review:
    t = Tokenizer()

    def __init__(self, score, text):
        global vocabulary
        self.score = score
        self.text = self._negate(self.t.tokenize(text))

        # add words from text to global vocabulary
        vocabulary.union(set(self.text))
        self.__count_sentiments()

    def __count_sentiments(self):
        global num_rev_pos, num_rev_neg, voc_pos, voc_neg
        if self.score == 1:
            num_rev_1 += 1
            for word in self.text:
                if word in voc_1:
                    voc_1[word] += 1
                else:
                    voc_1[word] = 1
        elif self.score == 2:
            num_rev_2 += 1
            for word in self.text:
                if word in voc_2:
                    voc_2[word] += 1
                else:
                    voc_2[word] = 1
        elif self.score == 3:
            num_rev_3 += 1
            for word in self.text:
                if word in voc_3:
                    voc_3[word] += 1
                else:
                    voc_3[word] = 1
        elif self.score == 4:
            num_rev_4 += 1
            for word in self.text:
                if word in voc_4:
                    voc_4[word] += 1
                else:
                    voc_4[word] = 1
        elif self.score == 5:
            num_rev_5 += 1
            for word in self.text:
                if word in voc_5:
                    voc_5[word] += 1
                else:
                    voc_5[word] = 1
        else:
            print('Error: Sentiment must be 1-5')

    def get_score(self):
        return self.score

    def get_text(self):
        return self.text

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


    def toString(self):
        return str(self.score) + ": " +  " ".join(self.text)


def parse_reviews(start_line, end_line):
    score = 0
    text = ""
    reviews = []
    curline = 0

    # clear screen
    print('                    ', end='\r')

    with open('SentimentTrainingData.txt', 'r') as f:
        # start at line start_line
        f.seek(start_line)

        for line in f.readlines():

            curline += 1

            # make sure we start the right place
            if(curline < start_line):
                continue

            if curline%1000 == 0:
                print('{0:.2%}'.format(1.0 / (end_line - start_line + 1) * (curline - start_line)), end='\r')

            if line[:14] == "review/score: ":
                score = int(line[14])
            if line[:16] == "review/summary: ":
                text += line[16:] + '.'
            if line[:13] == "review/text: ":
                text += line[13:]

                #Store and reset
                reviews.append(Review(score, text))
                text = ""

                # end read at line end_line
                if curline >= end_line:
                    break
    return reviews


### Sentiment stuff ####

# returns the probability of a list of reviews having a given sentiment
# if you are lost, look in slide 29
def prob_sentiment(sentiment):
    global num_rev_1, num_rev_2, num_rev_3, num_rev_4, num_rev_5
    n = sum([num_rev_1, num_rev_2, num_rev_3, num_rev_4, num_rev_5])

    if sentiment == 1:
        nc = num_rev_1
    elif sentiment == 2:
        nc = num_rev_2
    elif sentiment == 3:
        nc = num_rev_3
    elif sentiment == 4:
        nc = num_rev_4
    elif sentiment == 5:
        nc = num_rev_5
    else:
        nc = 0
        print("Error: prob_sentiment(sentiment) - sentiment must be 1-5")

    return (nc + 1)/(n + 5) # 2 is the number of classes (1, 2, 3, 4, 5)

# returns probability that a certain word has a given sentiment
# if you are lost, look in slide 29
def prob_word_in_sentiment(word, sentiment):
    global voc_1, voc_2, voc_3, voc_4, voc_5, vocabulary

    if sentiment == 1:
        nc = num_rev_pos
        if word in voc_pos:
            nxc = voc_1[word]
        else:
            nxc = 0 
    elif sentiment == 2:
        nc = num_rev_neg
        if word in voc_2:
            nxc = voc_neg[word]
        else:
            nxc = 0
    elif sentiment == 3:
        nc = num_rev_neg
        if word in voc_3:
            nxc = voc_neg[word]
        else:
            nxc = 0
    elif sentiment == 4:
        nc = num_rev_neg
        if word in voc_4:
            nxc = voc_neg[word]
        else:
            nxc = 0
    elif sentiment == 5:
        nc = num_rev_neg
        if word in voc_5:
            nxc = voc_neg[word]
        else:
            nxc = 0
    else:
        print("Error in prob_word_sentiment()!")
        return 0

    return (nxc + 1) / (nc + len(vocabulary))

def log_score (review, sentiment):
    pxc = 1

    for word in review.get_text():
        pxc *= prob_word_in_sentiment(word, sentiment) #log(prob_word_in_sentiment(word, sentiment))

    return prob_sentiment(sentiment) * pxc

def scoreTest(review):
    res = 1 if log_score(review, 1) > log_score(review, -1) else -1

    return res

#### this is where the fun stuff happens!

# parse reviews
#to_be_reviewed = parse_reviews(3000100, 3000100 + 1000000)

to_be_reviewed = []

to_be_reviewed.append(Review(-1, "The WORST coffee !. The worst!!! it is just plan awful bitter and strong and you cannot taste the Hazel Nut flavor at all!!!!!  Do not buy this product save your money!!!!!"))

vocabulary = set()
num_rev_1 = 0
num_rev_2 = 0
num_rev_3 = 0
num_rev_4 = 0
num_rev_5 = 0
voc_1 = {}
voc_2 = {}
voc_3 = {}
voc_4 = {}
voc_5 = {}
review_list = parse_reviews(1, 1000000)

total_hits = 0
cnt = 0;
total_reviews = len(to_be_reviewed)

# clear screen
print('                                       ', end='\r')

for rev in to_be_reviewed:
    score = scoreTest(rev)
    
    if(score == rev.get_score()):
        total_hits += 1

    cnt += 1
    print('{0:.2%}'.format(1.0 / total_reviews * cnt), end='\r')

print("Hit rate: ", (total_hits/total_reviews)*100, "%")