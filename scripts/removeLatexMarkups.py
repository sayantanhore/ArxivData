import re
import sys, os
import xml.etree.ElementTree as et
import isEnglish
from localsettings import *
import cprints as cp

# ------------------------------------------------------------------------------------------------------------------------------------------------

# Converts Equation markup to shorthand ($)
def change_eqn_markup_to_shorthand(s):
	s = s.replace("\\begin{equation}",  "$")\
	 	 .replace("\\end{equation}",    "$")\
	 	 .replace("\\begin{equation*}", "$")\
	 	 .replace("\\end{equation*}",   "$")
	cp.cprint("After changing math expressions to shorthand", s, True)
	return s


# Remove citations
def remove_citations(s):
	pattern = r'\\cite\{[^{}]*\}'
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("After removing citations", s, True)
	return s

# Removes equations
def remove_math_expr(s):
	#pattern = r'Set(?:Value)?'
	#pattern = r'(T|t)he'
	pattern = r'\$[^$]*\$'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("After removing math expressions", s, True)
	return s
	#pattern = r'[ ]?[A-Z]?[a-z]*[ ,.]'
	#pattern = r'[ ]?[A-Z]?[a-z]*(?=[ ,.<:])'

# Removes hyphens from the beginning of words
def remove_hyphen_from_start(s):
	pattern = r' -(?=[\w_]+[ ,;:?!.]?)'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	s = re.sub(pattern, " ", s, count = 0, flags = 0)
	cp.cprint("After removing hyphen from start", s, True)
	return s
	
# Count the number of words present
def count_words(s):
	#pattern = r'[^ <>/|\,.:\'"0-9][A-Za-z\-]*(?=[ ,.<:])'
	pattern = r'[\w-]+'
	res = re.findall(pattern, s)
	cp.cprint("Words present", res, True)
	cp.cprint("Total number of words after removal", str(len(res)), True)
	'''
	if res != None:
		print(res.group(0))
		print(res.groups())
	'''

# Reads the texts
def read_text(filename):
	text = open(filename, "r").read()
	return text

# Processes the extracted data
def process_data(s):
	cp.cprint("Original text", s, True)
	s = change_eqn_markup_to_shorthand(s)
	s = remove_math_expr(s)
	#text = "\cite{sds}dsdsad\cite{wewew33}sadsad sa sadsa dsa sa \cite{blah_blah} 5454875837584huhdbhfdsfy7 \cite{huahua}\cite{s}  uyegrewrewyrew	\cite{1222}	huhfuewuhf\cite{dsds}"
	#print(text)
	s = remove_citations(s)
	s = remove_hyphen_from_start(s)
	count_words(s)
	return s

# Reads the XML data file
def read_data(filename):
	cp.head("Processing, please wait ...")
	tree = et.parse(DATA_PATH + filename)
	root = tree.getroot()
	os.system('clear')
	for article in root.iter('article'):
		for id in article.iter('id'):
			if int(id.text) <= 5:
				cp.head("Document " + str(id.text) + " starts", True)
				text = article.find('abstract').text
				text = process_data(text)
				is_english = isEnglish.is_english(text)
				cp.cprint("Is the text in English?", is_english, True)
				isEnglish.correct_spelling(text)
				cp.head("Document " + str(id.text) + " ends", True)
				
				

if __name__ == '__main__':
	os.system('clear')
	read_data(sys.argv[1])
