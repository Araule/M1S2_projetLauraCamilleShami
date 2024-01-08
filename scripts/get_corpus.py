#!/usr/bin/env python
# coding: utf-8

import re
from tqdm import tqdm
from pathlib import Path
from datastructures import Corpus
from typing import Optional, List
from get_articles import to_article


months = ["Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug", 
          "Sep",
          "Oct",
          "Nov", 
          "Dec"]

days = [f"{x:02}" for x in range(1,32)]

dico_cat =  {	
            'une' : '0,2-3208,1-0,0', 
            'international' : '0,2-3210,1-0,0',
            'europe' : '0,2-3214,1-0,0', 
            'societe' :	'0,2-3224,1-0,0',
            'idees'	: '0,2-3232,1-0,0',
            'economie':	'0,2-3234,1-0,0',
            'actualite-medias':	'0,2-3236,1-0,0',
            'sport': '0,2-3242,1-0,0',
            'planete': '0,2-3244,1-0,0',
            'culture': '0,2-3246,1-0,0',
            'livres' : '0,2-3260,1-0,0',
            'cinema' : '0,2-3476,1-0,0',
            'voyage' : '0,2-3546,1-0,0',
            'technologies': '0,2-651865,1-0,0',
            'politique' : '0,57-0,64-823353,0',
            'sciences' : 'env_sciences'
            }

def convert_month(m:str) -> int:
   return months.index(m) + 1


def get_Corpus(fichiers:Path, nom_analyse: str, categories: Optional[List[str]]=None, begin: Optional[str]=None, end: Optional[str]=None):
    """ renvoie instance de Corpus
        Corpus(categories, begin, end, fichiers, liste_articles)
    """

    if categories is None or len(categories) == 0 :
        categories = dico_cat.keys() # si il n'y a pas de catégorie spécifiée, on prend toutes les catégories
    
    if begin is None :
        begin = "2022-01-01"
    if end is None :
        end = "2022-12-31"

    liste_articles = get_Article(chemins=fichiers, cat=categories, start_date=begin, end_date=end, nom_analyse=nom_analyse)

    return Corpus(categories, begin, end, fichiers, liste_articles)


def get_Article(chemins: Path, cat: List[str], start_date: str, end_date: str, nom_analyse: str):
    """ renvoie la liste d'instances d'Article
        liste_articles - list : [(date: str, article: Article)]
    """

    liste_articles = []
    total_articles = 0  # nombre total d'articles à traiter
    num_categories = [dico_cat[c] for c in cat]  # on a les valeurs et non plus les entrées du dictionnaire

    # compter le nombre total d'articles à traiter
    for month_directory in chemins.iterdir():
        if month_directory.name not in months:  # on ignore les dossiers qui ne sont pas des mois
            continue
        m = convert_month(month_directory.name)

        for day_directory in month_directory.iterdir():
            if day_directory.name not in days:  # on ignore les dossiers qui ne sont pas des jours
                continue

            date = f"2022-{m:02}-{day_directory.name}"  # on a une date au format ISO

            if (start_date is None or start_date <= date) and (end_date is None or end_date >= date):  # si la date se trouve dans le champ de recherche
                for time_directory in day_directory.iterdir():

                    if re.match(r"\d\d-\d\d-\d\d", time_directory.name):  # si le nom du fichier est bien au format ISO
                        for fichier in time_directory.iterdir():

                            if fichier.name.endswith(".xml") and any([c in fichier.name for c in num_categories]):  # si le fichier est bien un fichier xml et se trouve dans l'une des categories
                                total_articles += sum(1 for _ in to_article(fichier, nom_analyse, "", date))

    # traiter chaque article en affichant une barre de progression
    with tqdm(total=total_articles, unit="article") as pbar:
        for month_directory in chemins.iterdir():
            if month_directory.name not in months:  # on ignore les dossiers qui ne sont pas des mois
                continue
            m = convert_month(month_directory.name)

            for day_directory in month_directory.iterdir():
                if day_directory.name not in days:  # on ignore les dossiers qui ne sont pas des jours
                    continue

                date = f"2022-{m:02}-{day_directory.name}"  # on a une date au format ISO

                if (start_date is None or start_date <= date) and (end_date is None or end_date >= date):  # si la date se trouve dans le champ de recherche
                    for time_directory in day_directory.iterdir():

                        if re.match(r"\d\d-\d\d-\d\d", time_directory.name):  # si le nom du fichier est bien au format ISO
                            for fichier in time_directory.iterdir():

                                if fichier.name.endswith(".xml") and any([c in fichier.name for c in num_categories]):  # si le fichier est bien un fichier xml et se trouve dans l'une des categories
                                    nom_categorie = list(dico_cat.keys())[list(dico_cat.values()).index(fichier.stem)]

                                    for article in to_article(fichier, nom_analyse, nom_categorie, date):
                                        liste_articles.append(article)
                                        pbar.update(1)

    return liste_articles
