from happyfuntokenizing import Tokenizer

class Review:
    t = Tokenizer()

    def __init__(self, score, text):
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


    def toString(self):
        return str(self.score) + ": " +  " ".join(self.text)


def parse_reviews():
    score = 0
    text = ""
    reviews = []
    curline = 0
    with open('SentimentTrainingData.txt', 'r') as f:
        for line in f.readlines():
            curline += 1

            if curline%1000 == 0:
                print('{0:.2%}'.format(1.0/5026085*curline), end='\r')

            if line[:14] == "review/score: ":
                score = int(line[14])
            if line[:16] == "review/summary: ":
                text += line[16:]
            if line[:13] == "review/text: ":
                text += line[13:]

                #Store and reset
                reviews.append(Review(score, text))
                text = ""
                if curline > 100:
                    break
    return reviews

rev = parse_reviews()

print(rev[1].toString())
