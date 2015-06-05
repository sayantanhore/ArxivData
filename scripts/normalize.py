'''
Example pipeline for preprocessing. Normalizes the given text.
Under construction.
'''

from nltk.corpus import stopwords
import nltk
import pickle
import numpy as np
import re
import nltk
import string

def normalize(allwords):
        normallwords = allwords.lower()								#Lowercase
        normallwords = normallwords.encode('ascii','ignore')					#Clean encoding
        normallwords = re.sub('\\\cite.*?}','',normallwords, flags=re.DOTALL) 			#Remove \cite (no other latex yet)
	normallwords = normallwords.translate(normallwords.maketrans("",""), string.punctuation)#Remove punctuation
        intab = "0123456789"									#Example
        outtab = "          "									#Example cont.
        trantab = string.maketrans(intab, outtab)						#Example remove numbers
        normallwords = normallwords.translate(trantab)						#Example cont.
        #normallwords = [w for w in normallwords if not w in stopwords.words('english')]	#Remove stopwords
        return normallwords

