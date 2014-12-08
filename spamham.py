__author__ = 'nicky'

import sys

##########################################################################
#--------------------------- Reading in files ---------------------------#
#----------------------- also: feature extraction -----------------------#
##########################################################################

vocabularyFile = open('vocab_100000.wl', encoding = 'latin1')
vocabulary = {}
# creates a dictionary out of vocabulary with default value 0
for line in vocabularyFile:
    item = line.strip('\n')
    vocabulary[item] = 0
vocabularyFile.close()

spamTrainingFile = open('spam_training', encoding = 'latin1')
spamTrainingData = {}
# creates dict of spam training files !occurring in the vocabulary! and number of occurrences as key
for line in spamTrainingFile:
    item = line.strip('\n')
    if item in vocabulary.keys():
        if item not in spamTrainingData.keys():
            spamTrainingData[item] = 1
        else:
            spamTrainingData[item] += 1
spamTrainingFile.close()

hamTrainingFile = open('ham_training', encoding = 'latin1')
hamTrainingData = {}
# creates dict of ham training files !occurring in the vocabulary! and number of occurrences as key
for line in hamTrainingFile:
    item = line.strip('\n')
    if item in vocabulary.keys():
        if item not in hamTrainingData.keys():
            hamTrainingData[item] = 1
        else:
            hamTrainingData[item] += 1
hamTrainingFile.close()

testingFile = open('ham_spam_testing', encoding = 'latin1')
testingData = {}
#
email = 0
for line in testingFile:
    item = line.strip('\n')
    if '#*#*#' in item:
        email += 1
        testingData[email] = item[6:]

'''
    if item in vocabulary.keys():
        if item not in testingData.keys():
            testingData[item] = 1
        else:
            testingData[item] += 1
'''
testingFile.close()

##########################################################################
#-------------------------------- Counts --------------------------------#
##########################################################################

# discounting parameter
if len(sys.argv) > 1:
    d = sys.argv[1]
else:
    d = 0.7

# number of occurrences of all elements in spam
sumNSpam = 0
for element in spamTrainingData:
    sumNSpam += spamTrainingData[element]

# number of occurrences of all elements in ham
sumNHam = 0
for element in hamTrainingData:
    sumNHam += hamTrainingData[element]

# number of unique elements in spam
nPlusSpam = len(spamTrainingData)

# number of unique elements in ham
nPlusHam = len(hamTrainingData)

alphaSpam = d * nPlusSpam / sumNSpam
alphaHam = d * nPlusHam / sumNHam

##########################################################################
#------------------------ Smoothed probabilities ------------------------#
##########################################################################

# dictionary of smoothed probabilities of spam
spamTrainingDataProbability = {}
for item in spamTrainingData:
    spamTrainingDataProbability[item] = (spamTrainingData[item] - d) / sumNSpam + alphaSpam * (1 / len(vocabulary))

# dictionary of smoothed probabilities of ham
hamTrainingDataProbability = {}
for item in hamTrainingData:
    hamTrainingDataProbability[item] = (hamTrainingData[item] - d) / sumNHam + alphaHam * (1 / len(vocabulary))

##########################################################################
#------------------------------- The test -------------------------------#
##########################################################################

print(testingData)



'''
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
'''