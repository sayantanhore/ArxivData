import os
from path import *
# Global declarations
# --------------------------------------------------------

file_doc_group = "doc_group"
file_doc_id_text = "doc_id_text"
file_doc_id_text_updated = "doc_id_text_updated"

rows, columns = os.popen('stty size', 'r').read().split()
