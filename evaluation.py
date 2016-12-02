import math


##open cal similarity
file_s = open('output/senPairSimilarity.txt')
#file_s = open('output/tf-idf.txt')
try:
    sim = file_s.readlines()
finally:
    file_s.close()

##open training similarity
file_p = open('output/is_para_sen.txt')
try:
    is_para = file_p.readlines()
finally:
    file_p.close()


get = ""
line_sim = []
pos_test = 0
count = 0
for line in sim:
    get = ""
    for s in line:
        if s == '\t':
            if float(get) > 0.95:
                line_sim.append(1)
                pos_test += 1
            else:
                line_sim.append(0)
            count += 1
            break
        else:
            get += s

j = 0
pos_correct = 0
pos_real = 0
for line_p in is_para:
    if int(line_p[0]) == 1:
        pos_real += 1
        if line_sim[j] == 1:
            pos_correct += 1
    j += 1

print "correct detection "+ str(pos_correct)
print "test number of paraphrase " + str(pos_test)
print "real number of paraphrase " + str(pos_real)
print "total number of sentence pairs " + str(count)
print ""
print "precision is " + str((pos_correct*1.0)/pos_test)
print "recall is " + str((pos_correct*1.0)/pos_real)

