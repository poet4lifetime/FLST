__author__ = 'nicky'

vocabularyFile = open('vocab_100000.wl', encoding = 'latin1')
vocabulary = []

spamTrainingFile = open('spam_training', encoding = 'latin1')
spamTrainingData = {}

hamTrainingFile = open('ham_training', encoding = 'latin1')
hamTrainingData = {}

# creates list of vocabulary
for line in vocabularyFile:
    item = line.strip('\n')
    vocabulary.append(item)

for line in spamTrainingFile:
    item = line.strip('\n')
    if '#*#*#' in item:
        pass
    if item not in spamTrainingData.keys():
        spamTrainingData[item] = 1
    else:
        spamTrainingData[item] += 1

for line in hamTrainingFile:
    item = line.strip('\n')
    if '#*#*#' in item:
        pass
    if item not in hamTrainingData.keys():
        hamTrainingData[item] = 1
    else:
        hamTrainingData[item] += 1