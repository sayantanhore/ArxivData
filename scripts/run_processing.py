'''
This script is an example on how to use the preprocessing scripts in this folder.  
~80k arxiv documents in arxiv_cs.xml. (actual size 78129)
'''

import pickle
import scipy.io
import numpy as np

import extractXML
import normalize
import bagowords

def save_object(obj, filename):
	with open(filename, 'wb') as output:
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_object(filename): #EXAMPLE CODE HOW TO LOAD THE FILES (PICKLES)
        with open(filename, 'wb') as output:
                return pickle.load(output)
	
if __name__ == "__main__":
	abstracts = extractXML.extract_XML('arxiv_cs.xml')
	normallwords = normalize.normalize(abstracts)
	#wordmap = bagowords.generate_word_map(normallwords)
	#bagowords = bagowords.generate_bagowords(abstracts, wordmap)
	#scipy.io.write([wordmap,bagowords], 'bagowords.mat')
	data_bagowords = [wordmap, bagowords]
	data_abstracts =  normallwords
	save_object(data_bagowords, 'bagowords.pkl')
	save_object(data_abstracts, 'abstracts.pkl')
	
