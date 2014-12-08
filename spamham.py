__author__ = 'nicky'

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
        if '#*#*#' in item:
            pass
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

##########################################################################
#-------------------------------- Counts --------------------------------#
##########################################################################

# discounting parameter
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

spamTrainingDataProbability = {}
hamTrainingDataProbability = {}

for item in spamTrainingData:
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! check whether we need len vocab or len spamTrainData
    spamTrainingDataProbability[item] = (spamTrainingData[item] - d) / sumNSpam + alphaSpam * (1 / len(vocabulary))

    #check how max() works
    '''
    probability = max(spamTrainingData[item] - d, 0.0) / Nspam + ((d * nPlusSpam) / (Nspam * (len(spamTrainingData))))
    spamTrainingDataProbability[item] = probability
    '''

for item in hamTrainingData:
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! check whether we need len vocab or len hamTrainData
    hamTrainingDataProbability[item] = (hamTrainingData[item] - d) / sumNHam + alphaHam * (1 / len(vocabulary))

    #check how max() works
    '''
    probability = max(hamTrainingData[item] - d, 0.0) / Nham + ((d * nPlusHam) / (Nham * (len(hamTrainingData))))
    hamTrainingDataProbability[item] = probability
    '''

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