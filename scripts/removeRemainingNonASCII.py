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
# Removes braces
def remove_keywords(text):
	#pattern = r'(?<=\()[\w\- ]+(?=\))'
	#pattern = r'\w+[_\-]\w+|[A-Z]+[_\-]*[A-Z]+'
	pattern = r'(?:\w+[_\-]+)+\w+|(?:[A-Z]+[_\-]*)+[A-Z]+'
	#pattern = r'[A-Z]+'
	
	#print(text)
	#print("\n")
	cp.cprint("Removing Key-Words", "", True)
	cp.cprint("Patterns present", "", True)
	
	res = re.findall(pattern, text)
	
	print(res)
	print("\n")
	#text = re.sub(pattern, "", text, count = 0, flags = 0)
	for matched_str in res:
		if not ie.is_word(matched_str):
			pattern = r'[_\-]+'
			split_ups = re.split(pattern, matched_str)
			#text = text.replace(matched_str, )
			
			suggestion = ""

			for w in split_ups:
				if ie.is_word(w):
					suggestion += w
					suggestion += " "
			suggestion = suggestion.strip()
			text = text.replace(matched_str, suggestion)
	cp.cprint("After removal", "", True)
	print(text)
	print("\n")
	return text

# Removes math expressions not contained in dollar
def remove_braces(text):
	#pattern = r'(?:[]\w^~{}[/\+\*]+)+'
	#pattern = r'\(?\w*[][{}()^~_\-|/\+\*\d]+\w*\)?'
	pattern = r'\(+[\w\- ]*\)+'
	res = re.findall(pattern, text)
	#print(text)
	#print("\n")
	cp.cprint("Removing braces", "", True)
	cp.cprint("Patterns present", "", True)
	print(res)
	print("\n")
	#text = re.sub(pattern, "", text, count = 0, flags = 0)
	for matched_str in res:
		suggestion = matched_str.replace("(", "").replace(")", "")
		text = text.replace(matched_str, suggestion)
	cp.cprint("After removal", "", True)
	print(text)
	print("\n")
	return text

# Removes math expressions without dollar
def remove_math_without_dollar(text):
	pattern = r'\w*[][{}()^~_\-|/\+\*=\d]+\w*'
	res = re.findall(pattern, text)
	#print(text)
	#print("\n")
	cp.cprint("Removing Math expressions without dollar", "", True)
	cp.cprint("Patterns present", "", True)
	print(res)
	print("\n")
	text = re.sub(pattern, "", text, count = 0, flags = 0)
	cp.cprint("After removal", "", True)
	print(text)
	print("\n")
	return text

# Removes any non-alphabet chatacter left
def remove_non_alpha(text):
	pattern = r'[^\w\s.,;]+'
	res = re.findall(pattern, text)
	#print(text)
	#print("\n")
	cp.cprint("Removing Non-Alphabet characters", "", True)
	cp.cprint("Patterns present", "", True)
	print(res)
	print("\n")
	text = re.sub(pattern, "", text, count = 0, flags = 0)
	cp.cprint("After removal", "", True)
	print(text)
	print("\n")
	return text

if __name__ == '__main__':
	os.system('clear')
	cp.head("Reading data files ...")
	doc_group = json.load(open(DATA_PATH + "doc_group_2", "rb"))
	doc_id_text = json.load(open(DATA_PATH + "doc_id_text_2", "rb"))
	
	
	eng_docs = doc_group['eng'][:5]
	#generate_XML(eng_docs)
	#remove_math_expr_without_dollar()
	for index, value in enumerate(eng_docs):
		os.system('clear')
		cp.head("Scanning Document (" + str(value) + ") - " + str(index))
		text = doc_id_text[value]
		cp.cprint("Text", "", True)
		print(text)
		text = remove_keywords(text)
		text = remove_braces(text)
		text = remove_math_without_dollar(text)
		text = remove_non_alpha(text)
		doc_id_text[value] = text
		
		if (index % 1000) == 0:
			with open(DATA_PATH + file_doc_id_text_updated, "wb") as outfile:
				json.dump(doc_id_text, outfile)
	
	with open(DATA_PATH + file_doc_id_text_updated, "wb") as outfile:
		json.dump(doc_id_text, outfile)
	