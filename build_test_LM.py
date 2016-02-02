#!/usr/bin/python
import re
import nltk
import sys
import math
import getopt

#The threshold of misses allowed. Higher means more lenient
LMTHRESHOLD = 0.5

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    
    #initiate dictionaries for the three language models
    indo={}
    malay={}
    tamil={}
    
    LModel= [indo, malay, tamil]

    #Set of grams that appear in the LanguageModel(LM), used when smoothing later on.
    gramSet=set()
    
    with open(in_file, "r") as build_data:
        for line in build_data:
            # indonesian line
            if line[0] == "i":
                splitToGrams(line[11:len(line)], LModel[0], gramSet)     
            # malaysian line
            elif line[0] == "m":
                splitToGrams(line[10:len(line)], LModel[1], gramSet)
            # tamil line
            else:
                splitToGrams(line[6:len(line)], LModel[2], gramSet)
                
        addOneSmoothing(LModel, gramSet)
        populateCumulative(LModel)
        
    return LModel

"""
line is sentence from the file,
label is the resp. language dictionary,
gramSet is the set to store all grams that appear in the LM
"""
def splitToGrams(line, label, gramSet=None):
    #splits the sentence into 4char-grams, then adds to resp. dictionary
    for i in range(0,len(line)-3):
        #graminstance = list(line[i:i+4])
        graminstance = line[i:i+4]
        addToDict(graminstance, label, gramSet)

"""
gram is the instance of a 4char-gram
label is the resp.language dictionary
gramSet is the set to store all grams that appear in the LM
"""
def addToDict(gram, label, gramSet):
    gram = tuple(gram)
    label.setdefault(gram, 0)
    label[gram] += 1
    if gramSet != None:
        gramSet.add(gram)

"""
labelList is the list of Language Dictionaries
gramSet is the set of grams that appear in the LM
"""
def addOneSmoothing(labelList, gramSet):
    print "smoothing ..........................................................."
    for item in gramSet:
        for label in labelList:
            label.setdefault(item, 0)
            label[item] += 1        

"""
labelList is the list of Language Dictionaries
"""
def populateCumulative(labelList):
    print "calculating cumulative count of the grams in the LM........................................"
    for label in labelList:
        count_list = label.values()     
        label["cumulative"] = sum(count_list)

"""
label is the language dictionary
gramlist is the list of grams from the candidate sentence
"""
def calculateProb(label, gramlist):
    #calculates the probability that the candidate is of the language
    labelprob = 0
    notfound = 0
    cumulative = label["cumulative"]
    
    for gram in gramlist:
        prob = label.get(gram, 0)
        if prob == 0:
            notfound += 1;
        if prob > 0:
            labelprob += math.log10(float(prob)) - math.log10(cumulative)
    #ratio that the gram is not found in the LM to the number of grams
    #of the candidate sentence
    missratio= float(notfound)/len(gramlist)
    if  missratio > LMTHRESHOLD :
        return 0
    return labelprob        

def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below
    print "threshold set at ", LMTHRESHOLD
    output = open(out_file, "w")
    tempDict = {}
    with open(in_file, "r") as unlabeled:
        for line in unlabeled:
            splitToGrams(line, tempDict)
            grammed = tempDict.keys()
            indoprob = calculateProb(LM[0], grammed)    
            malayprob = calculateProb(LM[1], grammed)
            tamilprob = calculateProb(LM[2], grammed)
            maxprob = max(indoprob, malayprob, tamilprob)
            if maxprob == 0:
                label = "other"
            elif maxprob == indoprob:
                label = "indonesian"
            elif maxprob == malayprob:
                label = "malaysian"
            else:
                label = "tamil"
            output.write(label + " " + line)
            tempDict={}
    output.close()

"""      
def debugger(LM):
    print "size", len(LM[0]), len(LM[1]), len(LM[2])
    print "cumulative", LM[0]["cumulative"], LM[1]["cumulative"], LM[2]["cumulative"]
    for item in gramSet:
        print item, LM[0].get(item, 0), LM[1].get(item, 0), LM[2].get(item, 0)
"""

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
