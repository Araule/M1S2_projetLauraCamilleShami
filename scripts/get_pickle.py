#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pickle
import pprint
import pandas as pd

## Testé avec :
# python extract_corpus.py -s 2022-03-01 -e 2022-03-10  -f pickle ../corpus/2022/ sport

# Impression sur le terminal du contenu du fichier pickle
def read_pickle(pickled_file):
	obj = pickle.load(open(pickled_file, "rb"))
	pprint.pprint(obj)

# on imprime dans un fichier txt
def text_pickle(pickled_file):
	obj = pickle.load(open(pickled_file, "rb"))
	with open("out.txt", "a") as f:
    		pprint.pprint(obj, stream=f)
	


def to_pickle(corpus):
	pickle.dump(corpus, open(f'{corpus.begin}_{corpus.end}.pickle', 'wb'))
	
	# impression du contenu dans un fichier txt
	text_pickle(f'{corpus.begin}_{corpus.end}.pickle')
	#si affichage sur le terminale du fichier pickle
	#read_pickle(f'{corpus.begin}_{corpus.end}.pickle')
	




	
