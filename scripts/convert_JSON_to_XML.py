# This programme converts saved JSON datafile holding classification of abstracts into XML

# Author: Sayantan Hore


import xml.etree.ElementTree as et
import os, sys
import time
import json
import re
import isEnglish as ie

DATA_PATH = '/Users/sayantanhore/code/python/data/'

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
def remove_keywords():
	text = "We show that the globular cluster mass function (GCMF) in the Milky Way depends on cluster half-mass density (rho_h) in the sense that the turnover mass M_TO increases with rho_h while the width of the GCMF decreases. We argue that this is the expected signature of the slow erosion of a mass function that initially rose towards low masses, predominantly through cluster evaporation driven by internal two-body relaxation. We find excellent agreement between the observed GCMF -- including its dependence on internal density rho_h, central concentration c, and Galactocentric distance r_gc -- and a simple model in which the relaxation-driven mass-loss rates of clusters are approximated by -dM/dt = mu_ev ~ rho_h^{1/2}. In particular, we recover the well-known insensitivity of M_TO to r_gc. This feature does not derive from a literal ``universality'' of the GCMF turnover mass, but rather from a significant variation of M_TO with rho_h -- the expected outcome of relaxation-driven cluster disruption -- plus significant scatter in rho_h as a function of r_gc. Our conclusions are the same if the evaporation rates are assumed to depend instead on the mean volume or surface densities of clusters inside their tidal radii, as mu_ev ~ rho_t^{1/2} or mu_ev ~ x+y * Sigma_t^{3/4} -- alternative prescriptions that are physically motivated but involve cluster properties (rho_t and Sigma_t) that are not as well defined or as readily observable as rho_h. In all cases, the normalization of mu_ev required to fit the GCMF implies cluster lifetimes that are within the range of standard values (although falling towards the low end of this range). Our analysis does not depend on any assumptions or information about velocity anisotropy in the globular cluster system."
	#pattern = r'(?<=\()[\w\- ]+(?=\))'
	pattern = r'\w+[_\-]\w+|[A-Z]+[_\-]*[A-Z]+'
	#pattern = r'[A-Z]+'
	res = re.findall(pattern, text)
	print(text)
	print("\n")
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
			text = text.replace(matched_str, suggestion)
	print(text)
# Removes math expressions not contained in dollar
def remove_math_expr_without_dollar():
	text = "We show that the globular cluster mass function (GCMF) in the Milky Way depends on cluster half-mass density (rho_h) in the sense that the turnover mass M_TO increases with rho_h while the width of the GCMF decreases. We argue that this is the expected signature of the slow erosion of a mass function that initially rose towards low masses, predominantly through cluster evaporation driven by internal two-body relaxation. We find excellent agreement between the observed GCMF -- including its dependence on internal density rho_h, central concentration c, and Galactocentric distance r_gc -- and a simple model in which the relaxation-driven mass-loss rates of clusters are approximated by -dM/dt = mu_ev ~ rho_h^{1/2}. In particular, we recover the well-known insensitivity of M_TO to r_gc. This feature does not derive from a literal ``universality'' of the GCMF turnover mass, but rather from a significant variation of M_TO with rho_h -- the expected outcome of relaxation-driven cluster disruption -- plus significant scatter in rho_h as a function of r_gc. Our conclusions are the same if the evaporation rates are assumed to depend instead on the mean volume or surface densities of clusters inside their tidal radii, as mu_ev ~ rho_t^{1/2} or mu_ev ~ x+y * Sigma_t^{3/4} -- alternative prescriptions that are physically motivated but involve cluster properties (rho_t and Sigma_t) that are not as well defined or as readily observable as rho_h. In all cases, the normalization of mu_ev required to fit the GCMF implies cluster lifetimes that are within the range of standard values (although falling towards the low end of this range). Our analysis does not depend on any assumptions or information about velocity anisotropy in the globular cluster system."
	#pattern = r'(?:[]\w^~{}[/\+\*]+)+'
	pattern = r'\(?\w*[][{}()^~_\-|/\+\*\d]+\w*\)?'
	res = re.findall(pattern, text)
	print(text)
	print("\n")
	print(res)
	print("\n")
	text = re.sub(pattern, "", text, count = 0, flags = 0)
	print(text)

if __name__ == '__main__':
	os.system('clear')
	doc_group = json.load(open(DATA_PATH + "doc_group_2", "rb"))
	
	eng_docs = doc_group['eng'][:10]
	#generate_XML(eng_docs)
	#remove_math_expr_without_dollar()
	remove_keywords()
	
