# This programme converts saved JSON datafile holding classification of abstracts into XML

# Author: Sayantan Hore


import xml.etree.ElementTree as et
import os, sys
import time
import json
import re
import cprints as cp
import isEnglish as ie
from localsettings import *



def generate_XML(eng_docs):
	doc_id_text = json.load(open(DATA_PATH + "doc_id_text_2", "rb"))
	root = et.Element("articles")
	for idn in eng_docs:
		article = et.Element("article")
		article.set("language", "English")
		idno = et.SubElement(article, "id")
		idno.text = idn
		abstract = et.SubElement(article, "abstract")
		abstract.text = doc_id_text[idn]
		root.append(article)
	et.ElementTree(root).write("output.xml")

# Removes remaining latex opening constructs
def remove_latex_start(text):
	pattern = r'\\\w+\**\s*(?:(?:{[ \w*\\/|\-,;:]+}\s*)|(?:\[[ \w*\\/|\-,;:]+\]\s*)|(?:\([ \w\s,;:]+\)))*'
	cp.cprint("Removing Remaining Latex openings", "", True)
	cp.cprint("Patterns present", "", True)
	res = re.findall(pattern, text)
	print(res)
	print("\n")
	text = re.sub(pattern, " ", text, count = 0, flags = 0)
	print(text)
	print("\n")
	return text

# Removes any non-alphabet chatacter left
def remove_non_alpha(text):
	pattern = r'[\W\s.,;_-]+'
	res = re.findall(pattern, text)
	#print(text)
	#print("\n")
	cp.cprint("Removing Non-Alphabet characters", "", True)
	cp.cprint("Patterns present", "", True)
	print(res)
	print("\n")
	text = re.sub(pattern, " ", text, count = 0, flags = 0)
	cp.cprint("After removal", "", True)
	print(text)
	print("\n")
	return text

# Removes any non-alphabet chatacter left
def remove_non_word(text):
	pattern = r'[\w]+'
	res = re.findall(pattern, text)
	#print(text)
	#print("\n")
	#print(re.match(pattern, text))
	cp.cprint("Removing words", "", True)
	cp.cprint("Patterns present", "", True)
	print(res)
	print("\n")
	text = re.sub(pattern, produce_match_str, text, count = 0, flags = 0)
	cp.cprint("After removal", "", True)
	print(text)
	print("\n")
	return text

# Produces custom replacement for regex match
def produce_match_str(matched_word):
	match = matched_word.group(0)
	if not ie.is_word(match):
		return " "
	else:
		return match


if __name__ == '__main__':
	os.system('clear')
	cp.head("Reading data files ...")
	doc_group = json.load(open(DATA_PATH + file_doc_group, "rb"))
	doc_id_text = json.load(open(DATA_PATH + file_doc_id_text, "rb"))
	
	
	eng_docs = doc_group['eng'][:5]
	#generate_XML(eng_docs)
	#remove_math_expr_without_dollar()
	for index, value in enumerate(eng_docs):
		os.system('clear')
		cp.head("Scanning Document (" + str(value) + ") - " + str(index))
		text = doc_id_text[value]['text']
		cp.cprint("Text", "", True)
		print(text)
		text = remove_latex_start(text)
		text = remove_non_alpha(text)
		text = remove_non_word(text)
		doc_id_text[value]['text'] = text
		
		if (index % 1000) == 0:
			with open(DATA_PATH + file_doc_id_text_updated, "wb") as outfile:
				json.dump(doc_id_text, outfile)
	
	with open(DATA_PATH + file_doc_id_text_updated, "wb") as outfile:
		json.dump(doc_id_text, outfile)
	