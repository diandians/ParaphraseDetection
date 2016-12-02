from itertools import izip
import math
'''
    This document read pre-trained word vectors from selective corpus files.
    Then generate sentence vector using average word vectors, and save them in sen_vec.txt file
'''

#set dimension of word vector
CONST_NUM = 100

##use trie to save data
class TrieNode(object):
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.letters = {}
        self.vec = [0]*CONST_NUM

class Trie(object):

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, vector):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        temp = self.root
        for i, ch in enumerate(word):
            if ch not in temp.letters:
                temp.letters[ch] = TrieNode()
            temp = temp.letters[ch]
        temp.vec = vector
        temp.letters[1] = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        temp = self.root
        for ch in word:
            if ch in temp.letters:
                temp = temp.letters[ch]
            else:
                return temp.vec
        if 1 in temp.letters:
            return temp.vec
            
    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie
        that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        temp = self.root
        for ch in prefix:
            if ch in temp.letters:
                temp = temp.letters[ch]
            else:
                return False
        return True



##open word vector corpus
file_glove6B_100 = open('glove.6B\glove.6B.100d.txt')
try:
	word_vec_lines_100 = file_glove6B_100.readlines()
finally:
	file_glove6B_100.close()

##save word vector in trie
trie = Trie()
dimension = 0
for word in word_vec_lines_100:
    get = ""
    v = [] #vector
    w = "" #word
    dimension = 0
    for s in word:
        if s == ' ' or s == '\n':
            dimension += 1
            if dimension == 1:
                w = get
            else:
                v.append(float(get))
            get = ""
        else:
            get += s
    trie.insert(w, v)

##open microsoft corpus
file_micro = open('msr_data.txt')
try:
	train_lines = file_micro.readlines()
finally:
    file_micro.close()

##write output data
output = open('output/sen_vec.txt', 'w')
index = ""
i = -1
id1 = ""
id2 = ""
average = []
##find match word vector from word vector corpus
for string in train_lines:
    i += 1
    if i <= 0:
        continue
    word_str = ""
    sentenceSum = [0] * CONST_NUM
    sen_word_num = 0
    tab = 0
    wv_sum_max = 0
    wv_sum_fac = [1]
    for s in string:
        if s == ' ':
            word_str = word_str.lower()
            if trie.search(word_str) == None:
                wv = [0] * CONST_NUM
            else:
                wv = trie.search(word_str)
                #output.write(word_str + '\t')
                sen_word_num += 1
            sentenceSum = map(sum, izip(wv, sentenceSum))
            word_str = ""
        elif s == "\t":
            tab += 1
            if tab == 2:
                id1 = word_str
            elif tab == 3:
                id2 = word_str
            elif tab == 4:
                #finish this sentence
                word_str = word_str[:-1]
                word_str = word_str.lower()
                if trie.search(word_str) == None:
                    wv = [0] * CONST_NUM
                else:
                    wv = trie.search(word_str)
                    sen_word_num += 1
                sentenceSum = map(sum, izip(wv, sentenceSum))
                average = [x / sen_word_num for x in sentenceSum]
                #output.write(str(sen_word_num) + '\t')
                output.writelines(id1 + '\t' + str(average) + '\n')
                sentenceSum = [0] * CONST_NUM
                sen_word_num = 0
            word_str = ""
        elif s == '\n':
            # finish this sentence
            word_str = word_str[:-1]
            word_str = word_str.lower()
            if trie.search(word_str) == None:
                wv = [0] * CONST_NUM
            else:
                wv = trie.search(word_str)
                # add weight on word vector
                '''
                wv_sum = 0
                for wvi in range(0, CONST_NUM):
                    wv_sum += wv[wvi] * wv[wvi]
                if wv_sum > 5 * wv_sum_max:
                    wv_sum_max = wv_sum
                    wv_sum_fac.append(wv_sum_fac[-1] + 1)
                    '''
                sen_word_num += 1

            sentenceSum = map(sum, izip(wv, sentenceSum))
            average = [x / sen_word_num for x in sentenceSum]
            #output.write(str(sen_word_num) + '\t')
            output.writelines(id2 + '\t' + str(average) + '\n')
            word_str = ""
        else:
            word_str += s



##close output data file
output.close()
