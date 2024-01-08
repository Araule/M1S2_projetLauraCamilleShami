#!/usr/bin/env python
#-*- coding: utf-8 -*-

import feedparser
from datastructures import Article
from get_analyse import get_stanza, get_trankit, get_spacy

def which_analyse(nom_analyse, desc) :
    if nom_analyse == "stanza" :
        return get_stanza(desc)
    elif nom_analyse == "trankit" :
        return get_trankit(desc)
    else : # by default
        return get_spacy(desc)

def to_article(path, nom_analyse, nom_categorie, date) :
    d = feedparser.parse(path) # path = chemin du fichier
    for item in d.entries[::] : # pour chacune des entrées, c'est-à-dire des articles (entries en anglais)
        yield Article(item.title, item.description, date, nom_categorie, which_analyse(nom_analyse, item.description))
