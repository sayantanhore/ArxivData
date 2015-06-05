import re
import sys, os
import xml.etree.ElementTree as et

# Declarations
DATA_PATH = "/home/hore/code/data/"

# Converts Equation markup to shorthand ($)
def change_eqn_markup_to_shorthand(s):
	return s.replace("\\begin{equation}",  "$")\
	 		.replace("\\end{equation}",    "$")\
	 		.replace("\\begin{equation*}", "$")\
	 		.replace("\\end{equation*}",   "$")


# Remove citations
def remove_citations(s):
	pattern = r'\\cite\{[^{}]*\}'
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	return s

# Removes equations
def remove_equations(s):
	#pattern = r'Set(?:Value)?'
	#pattern = r'(T|t)he'
	pattern = r'\$[^$]*\$'
	res = re.findall(pattern, s)
	print(res)
	print("\n")
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	return s
	#pattern = r'[ ]?[A-Z]?[a-z]*[ ,.]'
	#pattern = r'[ ]?[A-Z]?[a-z]*(?=[ ,.<:])'
	
# Count the number of words present
def count_words(s):
	pattern = r'[^ <>/|\,.:\'"0-9][A-Za-z\-]*(?=[ ,.<:])'
	res = re.findall(pattern, s)
	print(res)
	print("Total number of words after removal :: " + str(len(res)))
	'''
	if res != None:
		print(res.group(0))
		print(res.groups())
	'''

# Reads the texts
def read_text(filename):
	text = open(filename, "r").read()
	return text

# Reads the XML data file
def read_data(filename):
	print("---------------------------")
	print("Processing, please wait ...")
	print("---------------------------")
	tree = et.parse(DATA_PATH + filename)
	root = tree.getroot()
	os.system('clear')
	for article in root.iter('article'):
		for id in article.iter('id'):
			if int(id.text) <= 1:
				text = article.find('abstract').text
				print(text)
				print("\n")
				text = change_eqn_markup_to_shorthand(text)
				print(text)
				text = remove_equations(text)
				print(text)
				print("\n")
				#text = "\cite{sds}dsdsad\cite{wewew33}sadsad sa sadsa dsa sa \cite{blah_blah} 5454875837584huhdbhfdsfy7 \cite{huahua}\cite{s}  uyegrewrewyrew	\cite{1222}	huhfuewuhf\cite{dsds}"
				#print(text)
				text = remove_citations(text)
				print(text)
				print("\n")
				
				

if __name__ == '__main__':
	'''
	filename = sys.argv[1]
	text = read_text(filename)
	#print(text)
	text = change_eqn_markup_to_shorthand(text)
	print(text)
	#remove_equations("The $ quick brown $ fox jumped $ over the $ lazy dog.")
	remove_equations(text)
	'''
	os.system('clear')
	read_data(sys.argv[1])
