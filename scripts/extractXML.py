'''
Extracts the data from the arxiv_cs.xml file. 
'''

import xml.etree.ElementTree as ET

def extract_XML(source):
        tree = ET.parse(source)
        root = tree.getroot()
        abstracts = []
        for neigh in root.iter('abstract'):
                abstracts.append(neigh.text)
        return abstracts

