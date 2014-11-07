from happyfuntokenizing import Tokenizer
from progressTrack import Progress

vocabulary = set()
num_rev_pos = 0
num_rev_neg = 0
voc_pos = {}
voc_neg = {}


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
            num_rev_pos += 1
            for word in self.text:
                if word in voc_pos:
                    voc_pos[word] += 1
                else:
                    voc_pos[word] = 1
        elif self.score == -1:
            num_rev_neg += 1
            for word in self.text:
                if word in voc_neg:
                    voc_neg[word] += 1
                else:
                    voc_neg[word] = 1
        else:
            print('Error: Sentiment must be 1 or -1')

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
        return str(self.score) + ": " + " ".join(self.text)


def parse_reviews(start_line, end_line):
    score = 0
    text = ""
    reviews = []
    cur_line = 0

    # clear screen
    print('                    ', end='\r')

    with open('SentimentTrainingData.txt', 'r') as f:
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
                if int(line[14]) < 3:  # only include non-neutral reviews
                    score = -1
                elif int(line[14]) > 3:
                    score = 1
                else:
                    continue

            if line[:16] == "review/summary: ":
                text += line[16:] + '.'
            if line[:13] == "review/text: ":
                text += line[13:]

                #Store and reset
                reviews.append(Review(score, text))
                text = ""

                # end read at line end_line
                if cur_line >= end_line:
                    break
    return reviews


### Sentiment stuff ####

# returns the probability of a list of reviews having a given sentiment
# if you are lost, look in slide 29
def prob_sentiment(sentiment):
    global num_rev_pos, num_rev_neg
    n = num_rev_pos + num_rev_neg

    if sentiment == 1:
        nc = num_rev_pos
    elif sentiment == -1:
        nc = num_rev_neg

    return (nc + 1)/(n + 2)  # 2 is the number of classes (true / false)

# returns probability that a certain word has a given sentiment
# if you are lost, look in slide 29
def prob_word_in_sentiment(word, sentiment):
    global voc_pos, voc_neg, vocabulary

    if sentiment == 1:
        nc = num_rev_pos
        if word in voc_pos:
            nxc = voc_pos[word]
        else:
            nxc = 0 
    elif sentiment == -1:
        nc = num_rev_neg
        if word in voc_neg:
            nxc = voc_neg[word]
        else:
            nxc = 0

    return (nxc + 1) / (nc + len(vocabulary))


def log_score (review, sentiment):
    pxc = 1

    for word in review.get_text():
        pxc *= prob_word_in_sentiment(word, sentiment)  #log(prob_word_in_sentiment(word, sentiment))

    return prob_sentiment(sentiment) * pxc


def scoreTest(review):
    res = 1 if log_score(review, 1) > log_score(review, -1) else -1

    return res

#### this is where the fun stuff happens!

# parse reviews
to_be_reviewed = parse_reviews(3000100, 3000100 + 1000000)

vocabulary = set()
num_rev_pos = 0
num_rev_neg = 0
voc_pos = {}
voc_neg = {}
review_list = parse_reviews(1, 300000)

total_hits = 0
cnt = 0
total_reviews = len(to_be_reviewed)

# clear screen
print('                                       ', end='\r')

p = Progress(total_reviews, "Computing scores")
for rev in to_be_reviewed:
    score = scoreTest(rev)
    
    if(score == rev.get_score()):
        total_hits += 1

    cnt += 1
    p.percent(cnt)

print("Hit rate: ", (total_hits/total_reviews)*100, "%")