# This file holds the scripts for - classifying abstracts into English and non-English groups, removing citations, math
# expressions, all begin-end constructs and grouping documents into a dictionary based on whether the previous constructs are
# present or not.

# Author: Sayantan Hore


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
doc_group = {}
doc_id_text = {}
counter = 0

file_doc_group = "doc_group"
file_doc_id_text = "doc_id_text"

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
	cp.cprint("Text before removing citations", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	pattern = r'\\cite\{[^{}]*\}'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		update_dict('cite', idn)
	else:
		update_dict('no-cite', idn)
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing citations", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s


# Removes equations
def remove_math_expr(idn, s, single = False):
	NO_MATH = False
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
		NO_MATH = False
	else:
		NO_MATH = True
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	s = remove_hyphen_from_start(s)
	cp.cprint("Text after removing math expressions", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s, NO_MATH

# Removes 'begin' markups
def remove_begin_markups(idn, s):
	NO_BEGIN = False
	cp.cprint("Text before removing begin constructs", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	pattern = r'\\begin\s*(?:(?:{\w+}\s*)|(?:\[\w+\]\s*))*'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		NO_BEGIN = False
	else:
		NO_BEGIN = True
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing begin constructs", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s, NO_BEGIN

# Removes 'end' markups
def remove_end_markups(idn, s):
	NO_END = False
	cp.cprint("Text before removing end constructs", s, True)
	cp.cprint("Word count before removal", "", True)
	count_words(s)
	pattern = r'\\end\s+{\w+}'
	res = re.findall(pattern, s)
	cp.cprint("Patterns present", res, True)
	print("\n")
	if len(res) > 0:
		NO_END = False
	else:
		NO_END = True
	s = re.sub(pattern, "", s, count = 0, flags = 0)
	cp.cprint("Text after removing end constructs", s, True)
	cp.cprint("Word count after removal", "", True)
	count_words(s)
	return s, NO_END


# Removes 'begin' constructs
def remove_begin_end_markups(idn, s):
	NO_BEGIN = False
	NO_END = False
	s, NO_BEGIN = remove_begin_markups(idn, s)
	s, NO_END = remove_end_markups(idn, s)
	if (NO_BEGIN == True) and (NO_END == True):
		update_dict('no-begin-end', idn)
	else:
		update_dict('begin-end', idn)
	return s
# Removes 'math' expressions, both $ and $$
def remove_math_expressions(idn, s):
	NO_MATH_SINGLE = False
	NO_MATH_DOUBLE = False
	# First pass
	s, NO_MATH_DOUBLE = remove_math_expr(idn, s, single = False)
	# Second pass
	s, NO_MATH_SINGLE = remove_math_expr(idn, s, single = True)
	if (NO_MATH_SINGLE is True) and (NO_MATH_DOUBLE is True):
		update_dict('no-math', idn)
	else:
		update_dict('math', idn)
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
	english = isEnglish.is_english(s)
	if english:
		cp.cprint("Language", "English")
		update_dict('eng', idn)
	else:
		cp.cprint("Language", "Non-English")
		update_dict('non-eng', idn)

# Update dictionary
def update_dict(key, idn):
	global doc_group
	if key not in doc_group.keys():
		doc_group[key] = [idn]
	else:
		doc_group[key].append(idn)

# Writes data to file
def write_to_file():
	global doc_group
	global doc_id_text
	with open(DATA_PATH + file_doc_group, "wb") as outfile:
		json.dump(doc_group, outfile)
	with open(DATA_PATH + file_doc_id_text, "wb") as outfile:
		json.dump(doc_id_text, outfile)

# Processes the extracted data
def process_data(idn, s):
	classify_docs(idn, s)
	s = remove_citations(idn, s)
	s = change_eqn_markup_to_shorthand(s)
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
				update_dict('total_docs', counter)
				write_to_file()
			if counter == 100:
				break
		elif event == 'start':
			tag = None
			if '' in dict(ns_map).keys():
				tag = elem.tag.replace('{' + dict(ns_map)[''] + '}', '')
			if tag == 'id':
				idn = elem.text
				os.system('clear')
				cp.head("Scanning Document (" + str(idn) + ") - " + str(counter))
			elif tag == 'abstract':
				text = elem.text
				if (text is not None) and (text.strip() != ""):
					cp.cprint("Original text", text, True)
					text = process_data(idn, text)
					doc_id_text[idn] = dict({'serial': counter, 'text': text})
					update_dict('text', idn)
				else:
					doc_id_text[idn] = dict({'serial': counter, 'text': ""})
					update_dict('no-text', idn)
					cp.cprint("Error", "No text found")
	update_dict('total_docs', counter)
	write_to_file()
if __name__ == '__main__':
	os.system('clear')
	read_data(sys.argv[1])
