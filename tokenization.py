'''
    this file tokenize raw sentences by removing punctuation, stop words and stemming.
'''


from nltk.stem.porter import *
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize

file_micro = open('msr_data.txt')
try:
	train_lines = file_micro.readlines()
finally:
    file_micro.close()

index = []
i = 0
all_documents = []
for line in train_lines:
    tab = 0
    get = ""
    i += 1
    if i == 1:
        continue
    for s in line:
        if s == '\t':
            tab += 1
            if tab <= 3 and tab > 1:
                index.append(get)
            elif tab > 3:
                all_documents.append(get.lower())
            get = ""
        elif s == '\n':
            all_documents.append(get.lower())
            get = ""
        else:
            get += s


##write output data
output = open('output/token.txt', 'w')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

#lower words and split sentence into words
tokenize = lambda doc: doc.lower().split(" ")
#remove non ascii characters
def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]',' ', text)


for i in range(0, all_documents.__len__()):
    all_documents[i] = remove_non_ascii_2(all_documents[i])
    #remove punctuation marks
    no_punctuation = all_documents[i].translate(None, string.punctuation)
    #split sentence into lowercase words
    tokens = word_tokenize(no_punctuation)
    #remove stop words
    filtered_sentence = [w for w in tokens if not w in stop_words]
    #stemming
    stem_words = [stemmer.stem(word) for word in filtered_sentence]
    stem_words = ' '.join(stem_words)
    output.write(str(index[i]) +'\t' + str(stem_words) + '\n')


output.close()