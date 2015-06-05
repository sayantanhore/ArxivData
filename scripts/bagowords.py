'''
NOT READY. Changing to sparse representation soon.
'''

import numpy as np

def generate_word_map(words):
        wordlist = set(words.split(' '))
        wordmapinv = dict()
        i = 0
        for word in wordlist:
                wordmapinv[i] = word
                i += 1
        wordmap = {v: k for k, v in wordmapinv.items()}
        return wordmap

def generate_bagowords(abstracts, wordmap): #FIX into sparse
        normal_abstracts = []
        for abstr in abstracts:
                normal_abstracts.append(normalize(abstr))
        bagowords = np.empty((len(wordmap),0),dtype='int64')
        for abstr in normal_abstracts:
                wordvec = np.zeros(len(wordmap))
                for word in abstr.split(' '):
                        wordvec[wordmap[word]] += 1
                bagowords = np.column_stack((bagowords,wordvec))
        return bagowords

