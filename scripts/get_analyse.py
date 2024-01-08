#!/usr/bin/env python
# coding: utf-8

import spacy
import stanza
from trankit import Pipeline
from datastructures import Token
from spacy.lang.fr.stop_words import STOP_WORDS


""" 
    format de sortie - list[Token] : [Token(form, lemma, pos), Token(form, lemma, pos), ...]
"""


def get_stanza(description) :
    
    stanza.download('fr') # download model
    nlp = stanza.Pipeline('fr') # download pipeline
    doc = nlp(description) # analyse the description
    stop_words = set(stanza.stopwords.words('fr'))  # get stop words
    liste_tokens = []  # list of tokens
    for item in doc.to_dict() : # double iteration
        for i in item :
            if i['text'].lower() not in stop_words:  # check if the token is not a stopword
                liste_tokens.append(Token(i['text'], i['lemma'], i['upos']))    
    return liste_tokens


def get_trankit(description, lang='french') :  # si la langue n'est pas spécifiée ce sera 'french' par défaut
    
    global p
    # Vérifie si le pipeline a déjà été téléchargé
    if not p:
        # Si p est None, le pipeline n'a pas encore été téléchargé, alors on le télécharge pour la langue spécifiée
        p = Pipeline(lang)

    # Analyse du texte avec le pipeline
    doc = p(description, is_sent=True)

    # Récupère les stopwords pour la langue spécifiée
    stopwords = set(trankit.Utils.get_stopwords(lang))

    # Crée une liste qui ressemblera à : [Token(forme='X', lemme='X', pos='X'), Token(...)] pour tous les mots de chaque phrase.
    tokens = []
    for token in doc['tokens']:

        # Vérifie si la forme en minuscule du token n'est pas un stopword
        if token['text'].lower() not in stopwords:

            # Crée un objet Token pour chaque token
            # Vérifie si le token a un lemme
            if 'lemma' in token:
                # Si oui, crée un objet Token avec le texte, le lemme et l'upos
                tokens.append(Token(token['text'], token['lemma'], token.get('upos', 'X'))) 
            else:
                # Sinon, crée un objet Token avec le texte, None comme lemme et l'upos
                tokens.append(Token(token['text'], None, token.get('upos', 'X')))

    return tokens


def get_spacy(description):
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(description)
    tokens = []
    for token in doc :
        if not token.is_stop:
            tokens.append(Token(token.text, token.lemma_, token.pos_))
    return tokens
