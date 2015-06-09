#!/bin/bash
#
# Usage: download the lemmatizer from 
#
# http://lemmatise.ijs.si/Download/File/Software%23LemmaGen_v2.0.zip
#
# also download the English lemmatizer model from
#
# http://lemmatise.ijs.si/Download/File/ModelData%23v2%23lem-m-en.zip
#
# put them in the same folder with this script
# run the script wit ha command such as "./lemmatizer '*.txt'" to lemmatize 
# all text files and save them with a '.lemmatized' extension

 
for f in $1
do
   ./lemmatize -l lem-me-en.bin $f $f.lemmatized
done
