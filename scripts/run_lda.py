#!/usr/bin/env python
#-*- coding: utf-8 -*-

r"""
LDA Model
=========

Introduces Gensim's LDA model and demonstrates its use on the NIPS corpus.

"""

"""
Exemple de commande pour lancer le script sur le terminal :
json :  
python scripts/run_lda.py /home/camille/Documents/Projet_M1TAL/PPE2-lauracamilleshami/2022-01-01_2022-03-01.json -f -l -p VERB -o /home/camille/Documents/Projet_M1TAL/PPE2-lauracamilleshami/resultats_lda.html
xml : 
python scripts/run_lda.py /home/camille/Documents/Projet_M1TAL/PPE2-lauracamilleshami/test.xml -f -l -p VERB -o /home/camille/Documents/Projet_M1TAL/PPE2-lauracamilleshami/resultats_lda.html
pickle:

"""

# commentaire sur le script : 
    # restreindre les données trop petites - j'avais essayé avec une 10 aines de jours, donne erreurs

from typing import List,Optional
import sys
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import re
import pickle
import json
import argparse
from xml.etree import ElementTree as ET

from gensim.models import Phrases
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

def load_xml(data_file, use_form=True, use_lemma=False, use_pos=None):
    with open(data_file, "r") as f:
        xml = ET.parse(f)
        docs = []
        for article in xml.findall(".//analyse"):
            doc = []
            for token in article.findall("./token"):
                if use_pos is None or token.attrib['pos'] in use_pos:
                    if use_lemma and 'lemme' in token.attrib and token.attrib['lemme'] != "":
                        label = token.attrib['lemme'].split('/')[0]
                    elif use_form and 'form' in token.attrib and token.attrib['form'] != "":
                        label = token.attrib['form']
                    else:
                        form = token.attrib.get('form', "")
                        lemma = token.attrib.get('lemme', "")
                        pos = token.attrib.get('pos', "")
                        if lemma != "":
                            label = lemma.split('/')[0]
                        elif form != "":
                            label = form
                        else:
                            label = None
                    
                    if label is not None:
                        doc.append(label)
                    else:
                        print("Attribut 'lemme' ou 'form' manquant ou vide pour le token :", token.attrib)
            
            if doc:
                docs.append(doc)
            else:
                print("La liste 'doc' est vide pour l'article :", article.attrib)
    
    return docs

def load_json(data_file, use_form=False, use_lemma=True, use_pos=None):
    """
    Extrait des documents d’un fichier JSON contenant des articles analysés.

    Parametres :
    data_file (str) : Chemin vers le fichier JSON.
    use_pos (str or None, optional (default=None)) : Si défini, utilise la partie du discours spécifiée (par exemple, "NOUN", "VERB", "ADJ") pour filtrer les mots dans le dictionnaire.
    use_lemma (bool, optional (default=True)) : Si True, utilise le lemme de la word comme clé dans le dictionnaire.
    use_form (bool, optional (default=False)) : Si True, utilise la forme de la word comme clé dans le dictionnaire.

    Returns :
    liste de str : liste de documents, où chaque document est une liste de chaînes représentant les jetons sélectionnés.
    """
    with open(data_file, "r") as f:
        data = json.load(f)
        docs = []
        # Parcours des articles
        for date, categories in data.items():
            for category, articles in categories.items():
                # Extraction des informations l'aide d'une expression régulière
                for title, article in articles.items():
                    analysis_str = article['Analyse']
                    tokens = re.findall(r"{form: (\w+), lemma: (\w+), pos: (\w+)}", analysis_str)
                    doc = []
                    # Parcours des tokens extraits et sélection des tokens selon les arguments passés
                    for token in tokens:
                        if use_pos is None or token[2] in use_pos:
                            if use_lemma:
                                doc.append(token[1])
                            if use_form:
                                doc.append(token[0])
                     # Ajout du document si celui-ci contient des tokens sélectionnés
                    if len(doc) > 0:
                        docs.append(doc)                     
        return docs
    
# get data from pickle file 
def load_pickle(data_file, use_form=True, use_lemma=False, use_pos=None):
    # data = Corpus read from pickle file
    data = pickle.load(open(data_file, "rb"))
    docs = []
    for article in data.articles:
        for Token in article.analyse:
            doc = []
            if use_pos is None or Token.pos in use_pos:
                if use_lemma:
                    doc.append(Token.lemme)
                if use_form:
                    doc.append(Token.forme)    
            if len(doc) > 0:
                docs.append(doc)    
    return docs
    
    
# Add bigrams and trigrams to docs (only ones that appear 20 times or more).

def add_bigrams(docs: List[List[str]], min_count=20):
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
    return docs

def build_lda_model(
        docs: List[List[str]],
        num_topics = 10,
        chunksize = 2000,
        passes = 20,
        iterations = 400,
        eval_every = None,
        no_below=20,
        no_above=0.5
        ):


    dictionary = Dictionary(docs)
    # Filter out words that occur less than 20 documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    print('Number of unique tokens: %d' % len(dictionary),sys.stderr)
    print('Number of documents: %d' % len(corpus))

    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token

    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every)
    return corpus, dictionary, model

def print_coherence(model, corpus):
    top_topics = model.top_topics(corpus)

# Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
    avg_topic_coherence = sum([t[1] for t in top_topics]) / model.num_topics
    print('\n\n\n\nAverage topic coherence: %.4f.' % avg_topic_coherence)

    from pprint import pprint
    pprint(top_topics)


def save_html_viz(model, corpus, dictionary, output_path):
    # ATTENTION, nécessite pandas en version 1.x
    # pip install pandas==1.5.*
    # (ce qui désinstallera pandas 2 si vous l'avez)
    # (d'où l'intérêt d'avoir un venv par projet) 
    vis_data = gensimvis.prepare(model, corpus, dictionary)
    with open(output_path, "w") as f:
        pyLDAvis.save_html(vis_data, f)

def main(corpus_file:str, num_topics, output_path: Optional[str]=None, show_coherence: bool=False):
    if ".json" in corpus_file :
        docs = load_json(corpus_file, args.use_form, args.use_lemma, args.use_pos)
    elif ".xml" in corpus_file : 
        docs = load_xml(corpus_file, args.use_form, args.use_lemma, args.use_pos)
    elif ".pickle" in corpus_file:
        docs = load_pickle(corpus_file, args.use_form, args.use_lemma, args.use_pos)
    else :
        print("\n\nformat du fichier non reconnu.\n\n")
    c, d, m = build_lda_model(docs, num_topics=num_topics)
    if output_path is not None:
        save_html_viz(m, c, d, output_path)
    if show_coherence:
        print_coherence(m, c)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('data_file', help='JSON file containing the data to process')
    parser.add_argument('-f', '--use-form', action='store_true', help='Filtre sur la forme du mot')
    parser.add_argument('-l', '--use-lemma', action='store_true', help='Filtre sur le lemme du mot')
    parser.add_argument('-p', '--use-pos', nargs='+', help='Filtre sur le POS pour le lemme et/ou la forme')  
    parser.add_argument('-t', '--topics', type=int, default=10, help='Nombre de topics dans le modèle LDA')
    parser.add_argument("-o", default=None, help="génère la visualisation ldaviz et la sauvegarde dans le fichier html indiqué")
    parser.add_argument("-c", action="store_true", default=False, help="affiche les topics et leur cohérence")
    """
    Les valeurs par défaut de 0.1 pour no_below et 0.9 pour no_above sont souvent utilisées car elles sont considérées comme des valeurs raisonnables
    pour éliminer les termes qui sont trop rares ou trop fréquents dans les documents.
    """
    parser.add_argument('--no_below', type=float, default=0.1,
                    help="Valeur minimale de fréquence d'apparition des mots dans le corpus (par défaut: 0.1)")
    parser.add_argument('--no_above', type=float, default=0.9,
                    help="Valeur maximale de fréquence d'apparition des mots dans le corpus (par défaut: 0.9)")
    args = parser.parse_args()
 
    # Si -p n'est pas fourni, use_pos sera None pour inclure toutes les parties du discours dans l'analyse.
    use_pos = args.use_pos if args.use_pos else None
    num_topics = args.topics
    no_below_value = args.no_below
    no_above_value = args.no_above

    main(args.data_file, num_topics, args.o, args.c)
