__author__ = 'alexei'

from nltk.corpus import stopwords as stop
import re

class User:

    def __init__(self):
        self.vocab = set()
        self.unique = set()

        self.word_count = 0

        # word count including stopwords
        self.word_count_total = 0

class Conversation:


    def __init__(self, file):
        self.lines = []
        self.parse_file(file)

    def parse_file(self, file):

        stopwords = stop.words('english')

        last_ts = -1
        time_deltas = []
        self.users = {}

        self.vocab = set()
        self.word_count = 0
        self.word_count_total = 0

        for line in open(file):

            parsed = line.strip().split()

            time = parsed[0]
            user = parsed[1].strip(":")
            line = parsed[2:]

            #print time, user, line

            if user not in self.users:
                self.users[user] = User()

            valid_words = [re.sub(r"[^a-zA-Z]", "", word.lower()) for word in line]
            self.users[user].word_count_total += len(valid_words)
            self.word_count_total += len(valid_words)

            relevant = [word for word in valid_words if word not in stopwords and len(word) > 1]

            if len(relevant) == 0:
                continue

            self.users[user].word_count += len(relevant)
            self.word_count += len(relevant)

            for word in relevant:
                self.users[user].vocab.add(word)

            min = int(time.split(":")[1])
            if last_ts != -1:
                if min != last_ts:
                    time_deltas.append(abs(min - last_ts))
            last_ts = min



        for user in self.users:
            user_blob = self.users[user]
            user_blob.unique = set(user_blob.vocab)

            for other in self.users:
                if user == other:
                    continue

                other_blob = self.users[other]
                user_blob.unique -= other_blob.vocab


        alpha = 0.65
        beta  = 0.35
        scores = []
        max, min = -1.0, -1.0


        for user in self.users:

            print "Stats for ", user
            blob = self.users[user]

            # print "Vocab: ", blob.vocab
            print "Vocab count: ", len(blob.vocab)

            print "Unique: ", blob.unique
            print "Unique count: ", len(blob.unique)

            print "Word count: ", blob.word_count
            print "Word count total (including stopwords): ", blob.word_count_total

            score = alpha * float(len(blob.unique)) + \
                    beta * float(blob.word_count_total) / float(blob.word_count)

            print "Score estimation: ", score

            self.vocab |= blob.vocab

            scores.append(score)
            if max == -1 or score > max:
                max = score
            if min == -1 or score < min:
                min = score

            print
#        print scores
#        print map(lambda x: float(x - 0) / float(10 - 0), scores)

        print "Conversation stats:"
        print "Vocab count: ", len(self.vocab)
        print "Word count: ", self.word_count
        print "Word count total (including stopwords): ", self.word_count_total
        print "Avg time gap between lines: ", float(sum(time_deltas)) / float(len(time_deltas))


def main():
    c = Conversation("./nlp.txt")

if __name__ == "__main__":
    main()