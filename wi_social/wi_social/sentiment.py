from happyfuntokenizing import Tokenizer
from math import log

vocabulary = set()

class Review:
    t = Tokenizer()

    def __init__(self, score, text):
        self.score = score
        self.text = self._negate(self.t.tokenize(text))

        # add words from text to global vocabulary
        vocabulary.union(set(self.text))

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
                if int(line[14]) < 3: # only include non-neutral reviews
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
                if curline >= end_line:
                    break
    return reviews


### Sentiment stuff ####

# returns the probability of a list of reviews having a given sentiment
# if you are lost, look in slide 29
def prob_sentiment(sentiment):
    nc = 0
    n = len(review_list)

    for review in review_list:
        if review.get_score() == sentiment:
            nc += 1

    return (nc + 1)/(n + 2) # 2 is the number of classes (true / false)

# returns probability that a certain word has a given sentiment
# if you are lost, look in slide 29
def prob_word_in_sentiment(word, sentiment):
    nxc = 0 + 1 
    nc = 0 + len(vocabulary)

    for review in review_list:
        if review.get_score() == sentiment:
           nc += 1
           if review.get_text().count(word):
               nxc += 1

    return nxc / nc

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
review_list = parse_reviews(1, 100000)
to_be_reviewed = parse_reviews(3000100, 3000100 + 300)

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