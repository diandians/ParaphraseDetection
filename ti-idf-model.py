from __future__ import division
import string
import math

file_micro = open('msr.txt')
try:
	train_lines = file_micro.readlines()
finally:
    file_micro.close()

all_documents = []
index = []

i = 0
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
                all_documents.append(get)
            get = ""
        elif s == '\n':
            all_documents.append(get)
            get = ""
        else:
            get += s



tokenize = lambda doc: doc.lower().split(" ")

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)

def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)

def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return (0.5 + ((0.5 * term_frequency(term, tokenized_document))/max_count))

def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents


########### END BLOG POST 1 #############

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude

tfidf_representation = tfidf(all_documents)
our_tfidf_comparisons = []


for doc in range(0, tfidf_representation.__len__(), 2):
    our_tfidf_comparisons.append(cosine_similarity(tfidf_representation[doc], tfidf_representation[doc+1]))


##write output data
output = open('output/tf-idf.txt', 'w')

p = 0
for x in our_tfidf_comparisons:
    output.write(str(x) + '\t')
    output.write(str(index[p]) + '\t')
    output.write(str(index[p+1]) + '\n')
    p += 2


#close output file
output.close()