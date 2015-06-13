import re
import sys, os
import time
import xml.etree.ElementTree as et
import isEnglish
from localsettings import *
import cprints as cp
import group_documents as gd
import json

# ------------------------------------------------------------------------------------------------------------------------------------------------
#Declarations
root = None
doc_group = {'eng': [], 'non-eng': []}



# Converts Equation markup to shorthand ($)
def change_eqn_markup_to_shorthand(s):
	s = s.replace("\\begin{equation}",  "$")\
	 	 .replace("\\end{equation}",    "$")\
	 	 .replace("\\begin{equation*}", "$")\
	 	 .replace("\\end{equation*}",   "$")
	cp.cprint("After changing math expressions to shorthand", s, True)
	return s


# Remove citations
def remove_citations(id, s):
	cp.cprint("Text before removing citations", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	pattern = r'\\cite\{[^{}]*\}'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		if 'cite' not in doc_group.keys():
			doc_group['cite'] = [id]
		else:
			doc_group['cite'].append(id)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing citations", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s


# Removes equations
def remove_math_expr(id, s, single = False):
	global doc_group
	if not single:
		cp.cprint("Checking for $$ MATH $$ expressions", "", True)
	else:
		cp.cprint("Checking for $ MATH $ expressions", "", True)
	cp.cprint("Text before removing math expressions", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	#pattern = r'\$[^$]*\$'
	if single == True:
		pattern = r'\$.*?\$'
	else:
		pattern = r'\$\$.*?\$\$'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		if 'math' not in doc_group.keys():
			doc_group['math'] = [id]
		else:
			doc_group['math'].append(id)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	s = remove_hyphen_from_start(s)
	cp.cprint("Text after removing math expressions", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s

# Removes 'begin' markups
def remove_begin_markups(id, s):
	global doc_group
	cp.cprint("Text before removing begin constructs", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	pattern = r'\\begin\s*(?:(?:{\w+}\s*)|(?:\[\w+\]\s*))*'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		if 'begin-end' not in doc_group.keys():
			doc_group['begin-end'] = [id]
		else:
			doc_group['begin-end'].append(id)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing begin constructs", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s

# Removes 'end' markups
def remove_end_markups(id, s):
	global doc_group
	cp.cprint("Text before removing end constructs", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	pattern = r'\\end\s+{\w+}'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		if 'begin-end' not in doc_group.keys():
			doc_group['begin-end'] = [id]
		elif id not in doc_group['begin-end']:
				doc_group['begin-end'].append(id)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing end constructs", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s


# Removes 'begin' constructs
def remove_begin_end_markups(id, s):
	'''
	global doc_group
	cp.cprint("Text before removing begin-end constructs", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	pattern = r'\\begin\s*(?:(?:{(\w+)})|(?:\[\w+\]))*\s*(?:\\item\s+[\w -,:;\'".]+\s+)+\\end\s*{\1}'
	#pattern = r''
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		if 'begin-end' not in doc_group.keys():
			doc_group['begin-end'] = [id]
		else:
			doc_group['begin-end'].append(id)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing begin-end constructs", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	'''
	s = remove_begin_markups(id, s)
	s = remove_end_markups(id, s)
	return s

# Removes hyphens from the beginning of words
def remove_hyphen_from_start(s):
	pattern = r' -(?=[\w_]+[ ,;:?!.]?)'
	res = re.findall(pattern, s)
	#cp.cprint("Patterns present", res, True)
	s = re.sub(pattern, " ", s, count = 0, flags = 0)
	#cp.cprint("After removing hyphen from start", s, True)
	return s
	
# Count the number of words present
def count_words(s):
	#pattern = r'[^ <>/|\,.:\'"0-9][A-Za-z\-]*(?=[ ,.<:])'
	pattern = r'[\w-]+'
	res = re.findall(pattern, s)
	#cp.cprint("Words present", res, True)
	cp.cprint("Total number of words", str(len(res)), False)
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
def process_data(id, s):
	s = remove_citations(id, s)
	s = change_eqn_markup_to_shorthand(s)
	s = remove_math_expr(id, s)
	s = remove_begin_end_markups(id, s)
	# Write to file
	if (id % 1000) == 0 or id == 78129:
		with open(DATA_PATH + "doc_grouped_latex.txt", "wb") as outfile:
			json.dump(doc_group, outfile)
		return s

# Reads the XML data file
def read_data(filename):
	cp.head("Processing, please wait ...")
	tree = et.parse(DATA_PATH + filename)
	global doc_group
	global root
	root = tree.getroot()
	os.system('clear')
	cp.head("Document root extracted")
	time.sleep(2)
	os.system('clear')

	#Classify documents
	if os.path.exists(DATA_PATH + "doc_grouped.txt"):
		doc_group = json.load(open(DATA_PATH + "doc_grouped.txt", "rb"))
	else:
		gd.group_docs(root, doc_group)
	
	# Process English documents
	documents = root.findall('article')
	cp.head("Starting to process documents in English")
	time.sleep(2)
	os.system('clear')
	for id in doc_group['eng']:
		if id < len(documents):
			cp.head("Document " + str(id) + " starts", True)
			text = documents[id - 1].find('abstract').text
			text = process_data(id, text)
			cp.head("Document " + str(id) + " ends", True)
	check_for = 'begin-end'
	if check_for in doc_group.keys():
		cp.cprint("Documents with begin-end expressions", doc_group[check_for])
	'''
	for article in root.iter('article'):
		id = article.find('id').text
		if int(id) <= 1:
			cp.head("Document " + str(id) + " starts", True)
			text = article.find('abstract').text
			text = process_data(text)
			is_english = isEnglish.is_english(text)
			cp.cprint("Is the text in English?", is_english, True)
			group_document(id, is_english)
			#isEnglish.correct_spelling(text)
			cp.head("Document " + str(id) + " ends", True)
		'''
	
	
	'''
	articles = root.findall('article')
	print(articles[2].find('abstract').text)
	#cp.cprint("The third text", root.find('article')[2].find('abstract').text)
	'''			

if __name__ == '__main__':
	os.system('clear')
	read_data(sys.argv[1])
