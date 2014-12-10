'''
Group Names:
Aniko Kovacs, Matriculation #: 2556570
Alena Vasilevich, Matriculation #: 2556836
Tyler Klement, Matriculation #: 2556065
'''

import sys
from math import log

##########################################################################
#--------------------------- Reading in files ---------------------------#
#----------------------- also: feature extraction -----------------------#
##########################################################################

vocabularyFile = open('vocab_100000.wl', encoding='latin1')
vocabulary = {}
# creates a dictionary out of vocabulary with default value 0
for line in vocabularyFile:
    item = line.strip('\n')
    vocabulary[item] = 0
vocabularyFile.close()

countSpamInTrain = 0

spamTrainingFile = open('spam_training', encoding='latin1')
spamTrainingData = {}
# creates dict of spam training files !occurring in the vocabulary! and number of occurrences as key
for line in spamTrainingFile:
    item = line.strip('\n')
    if '#*#*#' in item:
        countSpamInTrain += 1
    if item in vocabulary.keys():
        if item not in spamTrainingData.keys():
            spamTrainingData[item] = 1
        else:
            spamTrainingData[item] += 1
spamTrainingFile.close()

countHamInTrain = 0

hamTrainingFile = open('ham_training', encoding='latin1')
hamTrainingData = {}
# creates dict of ham training files !occurring in the vocabulary! and number of occurrences as key
for line in hamTrainingFile:
    item = line.strip('\n')
    if '#*#*#' in item:
        countHamInTrain += 1
    if item in vocabulary.keys():
        if item not in hamTrainingData.keys():
            hamTrainingData[item] = 1
        else:
            hamTrainingData[item] += 1
hamTrainingFile.close()

testingFile = open('ham_spam_testing', encoding='latin1')
testFile = ''
# removes newline character and adds spaces between words
for line in testingFile:
    line = line.strip('\n')
    testFile += str(line) + ' '
# splits testfile into list of emails
testFile = testFile.split(" #*#*#")
# splits emails into lists of words
for item in range(len(testFile)):
    testFile[item] = testFile[item].strip(" ").split(" ")
# list of emails with lists of words !occuring in the vocabulary! + class at index [0]
for item in testFile:
    for element in item:
        if element not in vocabulary.keys():
            if "#*#*#"in element:
                pass
            else:
                item[:] = (x for x in item if x != element)
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

# backoff
alphaSpam = (d * nPlusSpam / sumNSpam) * (1 / len(vocabulary))
alphaHam = (d * nPlusHam / sumNHam) * (1 / len(vocabulary))

# class probabilities
spamClassProbability = countSpamInTrain / (countSpamInTrain + countHamInTrain)
print("Spam class prob:", spamClassProbability)
hamClassProbability = countHamInTrain / (countSpamInTrain + countHamInTrain)
print("Ham class prob:", hamClassProbability)

##########################################################################
#------------------------ Smoothed probabilities ------------------------#
##########################################################################

# dictionary of smoothed probabilities of spam
spamTrainingDataProbability = {}
for item in spamTrainingData:
    tmp = spamTrainingData[item] - d
    if tmp < 0:
        tmp = 0
    spamTrainingDataProbability[item] = tmp / sumNSpam + alphaSpam

# dictionary of smoothed probabilities of ham
hamTrainingDataProbability = {}
for item in hamTrainingData:
    tmp = hamTrainingData[item] - d
    if tmp < 0:
        tmp = 0
    hamTrainingDataProbability[item] = tmp / sumNHam + alphaHam

##########################################################################
#------------------------------- The test -------------------------------#
##########################################################################

count = 0
misClassSpamToHam = 0
misClassHamToSpam = 0
hamList = []
spamList = []
unknownList = []

for email in testFile:
    hamProbability = 0
    spamProbability = 0
    for word in email:
        if word == 'spam' or word == 'ham':
            pass
        else:
            if word in hamTrainingDataProbability.keys():
                hamProbability += log(hamTrainingDataProbability[word])
            elif word not in hamTrainingDataProbability.keys():
                hamProbability += log(alphaHam)
            if word in spamTrainingDataProbability.keys():
                spamProbability += log(spamTrainingDataProbability[word])
            elif word not in spamTrainingDataProbability.keys():
                spamProbability += log(alphaSpam)
    # adding factor of class probability
    hamProbability += log(hamClassProbability)
    spamProbability += log(spamClassProbability)
    if hamProbability > spamProbability:
        hamList.append((email, 'ham'))
    elif spamProbability > hamProbability:
        spamList.append((email, 'spam'))
    else:
        unknownList.append((email, 'unknown'))

print("Ham list length:", len(hamList))
print("Spam list length:", len(spamList))
print("Unknown list length:", len(unknownList))

for tuplePair in hamList:
    if tuplePair[0][0] == 'spam':
        misClassSpamToHam += 1

for tuplePair in spamList:
    if tuplePair[0][0] == 'ham':
        misClassHamToSpam += 1

print("Misclassified spam to ham:", misClassSpamToHam)
print("Misclassified ham to spam:", misClassHamToSpam)