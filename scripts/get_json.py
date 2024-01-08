#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json

def to_json(corpus):
    # Crée un dictionnaire vide pour stocker les données
    data = {}

    # Itère sur les articles dans le corpus
    for article in corpus.articles :

        date_key = article.date

        # Extrait la catégorie de l'article
        cat_key = article.categorie

        # Ajoute la catégorie au dictionnaire de données si elle n'existe pas déjà
        if date_key not in data:
            data[date_key] = {}

        if cat_key not in data[date_key]:
            data[date_key][cat_key] = {}

        # Ajoute l'article au dictionnaire de données
        description = article.description
        analyse = ', '.join([f'{{form: {token.forme}, lemma: {token.lemme}, pos: {token.pos}}}' for token in article.analyse])
        data[date_key][cat_key][f"Titre : {article.titre}"] = {"Description": description, "Analyse": analyse}

    # Écriture des données dans un fichier JSON
    with open(f"{corpus.begin}_{corpus.end}.json", "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
