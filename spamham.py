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

for values in spamTrainingData:
    totalSpamCount += spamTrainingData[values]

probabilityOfElementInSpam = spamTrainingData[item]/totalSpamCount

# number of instances in ham
totalHamCount = 0

for values in hamTrainingData:
    totalHamCount += hamTrainingData[values]

print(totalHamCount)

probabilityOfElementInHam = hamTrainingData[item]/totalHamCount
