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
doc_id_text = {}
counter = 0

file_doc_group = "doc_group_2"
file_doc_id_text = "doc_id_text_2"

# Converts Equation markup to shorthand ($)
def change_eqn_markup_to_shorthand(s):
	s = s.replace("\\begin{equation}",  "$")\
	 	 .replace("\\end{equation}",    "$")\
	 	 .replace("\\begin{equation*}", "$")\
	 	 .replace("\\end{equation*}",   "$")
	cp.cprint("After changing math expressions to shorthand", s, True)
	return s


# Remove citations
def remove_citations(idn, s):
	global doc_group
	cp.cprint("Text before removing citations", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	pattern = r'\\cite\{[^{}]*\}'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		if 'cite' not in doc_group.keys():
			doc_group['cite'] = [idn]
		else:
			doc_group['cite'].append(idn)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing citations", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s


# Removes equations
def remove_math_expr(idn, s, single = False):
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
		pattern = r'\$[^$]*\$'
	else:
		pattern = r'\$\$[^$]*\$\$'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		if 'math' not in doc_group.keys():
			doc_group['math'] = [idn]
		elif idn not in doc_group['math']:
			doc_group['math'].append(idn)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	s = remove_hyphen_from_start(s)
	cp.cprint("Text after removing math expressions", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s

# Removes 'begin' markups
def remove_begin_markups(idn, s):
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
			doc_group['begin-end'] = [idn]
		else:
			doc_group['begin-end'].append(idn)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing begin constructs", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s

# Removes 'end' markups
def remove_end_markups(idn, s):
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
			doc_group['begin-end'] = [idn]
		elif idn not in doc_group['begin-end']:
			doc_group['begin-end'].append(idn)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing end constructs", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s


# Removes 'begin' constructs
def remove_begin_end_markups(idn, s):
	s = remove_begin_markups(idn, s)
	s = remove_end_markups(idn, s)
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

# Classifies documents into language groups
def classify_docs(idn, s):
	global doc_group
	english = isEnglish.is_english(s)
	if english:
		cp.cprint("Language", "English")
		doc_group['eng'].append(idn)
	else:
		cp.cprint("Language", "Non-English")
		doc_group['non-eng'].append(idn)

# Processes the extracted data
def process_data(idn, s):
	classify_docs(idn, s)
	s = remove_citations(idn, s)
	s = change_eqn_markup_to_shorthand(s)
	s = remove_math_expr(idn, s, single = False)
	# Second pass
	s = remove_math_expr(idn, s, single = True)
	s = remove_begin_end_markups(idn, s)
	return s


# Reads the XML data file
def read_data(filename):
	cp.head("Processing, please wait ...")
	time.sleep(2)
	#tree = et.parse(DATA_PATH + filename)
	idn = None
	text = ""
	ns_map = []
	global counter
	global doc_group
	global doc_id_text
	for event, elem in et.iterparse(DATA_PATH + filename, events = ('start', 'start-ns', 'end-ns')):
		if event == 'start-ns':
			ns_map.append(elem)
			if len(ns_map) == 2:
				counter += 1
		elif event == 'end-ns':
			ns_map.pop()
			# Write to file
			if (counter % 1000) == 0:
				with open(DATA_PATH + file_doc_group, "wb") as outfile:
					json.dump(doc_group, outfile)
				with open(DATA_PATH + file_doc_id_text, "wb") as outfile:
					json.dump(doc_id_text, outfile)
			#if counter == 10:
				#break
		elif event == 'start':
			tag = None
			if '' in dict(ns_map).keys():
				tag = elem.tag.replace('{' + dict(ns_map)[''] + '}', '')
			if tag == 'id':
				idn = elem.text
				os.system('clear')
				cp.head("Scanning Document " + str(counter))
			elif tag == 'abstract':
				text = elem.text
				if text is not None:
					cp.cprint("Original text", type(text), True)
					text = process_data(idn, text)
					doc_id_text[idn] = text
				else:
					if 'no-text' not in doc_group.keys():
						doc_group['no-text'] = [idn]
					else:
						doc_group['no-text'].append(idn)
					cp.cprint("Error", "No text found")

	with open(DATA_PATH + file_doc_group, "wb") as outfile:
		json.dump(doc_group, outfile)

	with open(DATA_PATH + file_doc_id_text, "wb") as outfile:
		json.dump(doc_id_text, outfile)
if __name__ == '__main__':
	os.system('clear')
	read_data(sys.argv[1])
