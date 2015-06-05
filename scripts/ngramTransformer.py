# This script will read in a corpus, look for all frequently occurring
# 2-grams and 3-grams, and then process the corpus so as to combine them.
# E.g. all occurrances of "machine learning" will be combined into
# "machine_learning".
#
# Mallet users: Mallet normally treats underlines as spaces, so if you
# don't want Mallet to just throw away all the work this script does,
# add the "--token-regex "[\p{Alpha}_]+"" parameter when importing the
# n-grammed corpus into Mallet.
#
# Possible stopword removal should be done BEFORE running this script.
#
# For configuration, see the constants below.
#
# Author: Kaj Sotala

def processGrams(gen, filelist):
    if EDIT_FILES:
        transformFiles(gen, filelist)
    else:
        printGrams(gen)

def printGrams(gen):
    for gram in gen:
        before = " ".join(gram)
        after = "_".join(gram)
        print before + " would be joined into " + after

def transformFiles(gen, filelist):
    gramlist = list(gen)
    i = 0
    for filename in filelist:
        i += 1
        print "Processing file " + str(i) + "/" + str(len(filelist))
        f1 = open(filename, 'r')
        f2 = open(filename + ".tmp", 'w')
        for line in f1:
            for gram in gramlist:
                    before = " ".join(gram)
                    after = "_".join(gram)
                    line = line.replace(before, after)
            f2.write(line)
        f1.close()
        f2.close()
        os.remove(filename)
        os.rename(filename + ".tmp", filename)

# combine into single words any n-grams with at least this
# level of Pointwise Mutual Information
MIN_2GRAM_PMI = 3
MIN_3GRAM_PMI = 2

# ignore any n-grams that appear less often than this
MIN_FREQUENCY = 100

# Whether to actually modify any files. If false, the script will only
# print stopwords that _would_ have been joined together had the variable
# been true instead. (For evaluating different minimum thresholds.)
EDIT_FILES = True

# what files to read and from where
CORPUS_ROOT = '/home/ksotala/Hiit/mallet-2.0.7/dataset/lemmatized/nostop2/'
CORPUS_EXTENSION =r'.*\.txt'

import nltk
import os
from os import listdir
from os.path import isfile, join
from nltk.collocations import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

# read in corpus, find all the 3-grams above the min frequency
print "Reading in corpus from", CORPUS_ROOT
my_corpus = PlaintextCorpusReader(CORPUS_ROOT, CORPUS_EXTENSION)
print "Read in " + str(len(my_corpus.fileids())) + " files"
print "Finding 3-grams"
finder_3gram = TrigramCollocationFinder.from_words(my_corpus.words())
print "Filtering out 3-grams of frequency less than", MIN_FREQUENCY
finder_3gram.apply_freq_filter(MIN_FREQUENCY)

# combine all the 3-grams meeting the PMI threshold
print "Looking for 3-grams with a PMI of at least ", MIN_3GRAM_PMI
filelist = [ join(CORPUS_ROOT,f) for f in listdir(CORPUS_ROOT) if isfile(join(CORPUS_ROOT,f)) ]
gen = finder_3gram.above_score(trigram_measures.pmi, MIN_3GRAM_PMI)
processGrams(gen, filelist)

# now let's do the same for the 2-grams
# our previous step altered the corpus so let's read it in again
print "Reading in corpus from", CORPUS_ROOT
my_corpus = PlaintextCorpusReader(CORPUS_ROOT, CORPUS_EXTENSION)
print "Finding 2-grams"
finder_2gram = BigramCollocationFinder.from_words(my_corpus.words())
print "Filtering out 2-grams with frequency less than", MIN_FREQUENCY
finder_2gram.apply_freq_filter(MIN_FREQUENCY)

print "Looking for 2-grams with a PMI of at least", MIN_2GRAM_PMI
gen = finder_2gram.above_score(bigram_measures.pmi, MIN_2GRAM_PMI)
processGrams(gen, filelist)
