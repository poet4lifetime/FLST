__author__ = 'nicky'


vocabularyFile = open('vocab_100000.wl', encoding = 'latin1')
vocabulary = []

# creates list of vocabulary
for line in vocabularyFile:
    item = line.strip('\n')
    vocabulary.append(item)

vocabularyFile.close()


spamTrainingFile = open('spam_training', encoding = 'latin1')
spamTrainingData = {}

# creates dict of spam training files and freq as key
for line in spamTrainingFile:
    item = line.strip('\n')
    if '#*#*#' in item:
        pass
    if item not in spamTrainingData.keys():
        spamTrainingData[item] = 1
    else:
        spamTrainingData[item] += 1

spamTrainingFile.close()


hamTrainingFile = open('ham_training', encoding = 'latin1')
hamTrainingData = {}

# creates dict of ham training files and freq as key
for line in hamTrainingFile:
    item = line.strip('\n')
    if '#*#*#' in item:
        pass
    if item not in hamTrainingData.keys():
        hamTrainingData[item] = 1
    else:
        hamTrainingData[item] += 1

hamTrainingFile.close()

# number of instances in spam
totalSpamCount = 0
'''
for values in spamTrainingData:
    totalSpamCount += spamTrainingData[values]

probabilityOfElementInSpam = spamTrainingData[item]/totalSpamCount

# number of instances in ham
totalHamCount = 0

for values in hamTrainingData:
    totalHamCount += hamTrainingData[values]

print(totalHamCount)

probabilityOfElementInHam = hamTrainingData[item]/totalHamCount
'''

nPlusHam = 0
nPlusSpam = 0
Nspam = 0
Nham = 0
d = 0.7

# smoothing

spamTrainingDataProbability = {}
hamTrainingDataProbability = {}

for item in spamTrainingData:
    Nspam += spamTrainingData[item]
    if spamTrainingData[item] > 0:
        nPlusSpam += 1
    probability = max(spamTrainingData[item] - d, 0.0) / Nspam + ((d * nPlusSpam) / (Nspam * (len(spamTrainingData))))
    spamTrainingDataProbability[item] = probability

for item in hamTrainingData:
    Nham += hamTrainingData[item]
    if hamTrainingData[item] > 0:
        nPlusHam += 1
    probability = max(hamTrainingData[item] - d, 0.0) / Nham + ((d * nPlusHam) / (Nham * (len(hamTrainingData))))
    hamTrainingDataProbability[item] = probability

classOfItem = {}

for item in vocabulary:
    if item in hamTrainingDataProbability.keys():
        if item in spamTrainingDataProbability.keys():
            if hamTrainingDataProbability[item] > spamTrainingDataProbability[item]:
                classOfItem[item] = 'ham'
            elif spamTrainingDataProbability[item] > hamTrainingDataProbability[item]:
                classOfItem[item] = 'spam'
        else:
            pass
    else:
        pass

print(classOfItem)