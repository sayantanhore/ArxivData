# This programme helps grouping the documents between English and Non English

import xml.etree.ElementTree as et
import isEnglish
import cprints as cp
import os, time

# Separates English and Non-English documents
def group_docs(root, doc_group):
	cp.head("Running language check", False)
	time.sleep(1)
	os.system('clear')
	for article in root.iter('article'):
		id = int(article.find('id').text)
		if id <= 10:
			cp.head("Checking document " + str(id))
			english = isEnglish.is_english(article.find('abstract').text)
			if english:
				doc_group['eng'].append(id)
			else:
				doc_group['non-eng'].append(id)
			os.system('clear')
	cp.head("Classification completed")
	cp.cprint("How many", "", True)
	cp.cprint("English", len(doc_group['eng']))
	cp.cprint("Non-English", len(doc_group['non-eng']))
	time.sleep(1)
	os.system('clear')