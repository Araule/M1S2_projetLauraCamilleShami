#!/usr/bin/env python
#-*- coding: utf-8 -*-

import argparse
from pathlib import Path
from get_xml import to_xml
from get_pickle import to_pickle
from get_json import to_json
from get_corpus import get_Corpus


''' 
    exemple de ce que l'on peut taper sur le terminal : 
    python scripts/extract_corpus.py 
    -s 2022-XX-XX 
    -e 2022-XX-XX 
    -m <spacy ou trankit ou stanza> 
    -f <xml ou json ou pickle>
    ~/Documents/PPE2-lauracamilleshami/corpus/2022/ 
    < rien ou (par ex) une international sport planete>
'''
                   

parser = argparse.ArgumentParser()
parser.add_argument("-s", help="start date (iso format)", default="2022-01-01")
parser.add_argument("-e", help="end date (iso format)", default="2023-01-01")
parser.add_argument("-m", help="choix de l'analyse syntaxique")
parser.add_argument("-f", help="choix du format de sortie")
parser.add_argument("fichiers", help="root dir of the corpus data")
parser.add_argument("categories",nargs="*", help="catégories à retenir")
args = parser.parse_args()


# on crée notre instance Corpus
corpus = get_Corpus(fichiers=Path(args.fichiers),
                    nom_analyse=args.m, 
                    categories=args.categories, 
                    begin=args.s,
                    end=args.e)

if args.f == "json" :
    to_json(corpus)
elif args.f == "pickle" :
    to_pickle(corpus)
else : # by default
    to_xml(corpus)
