#!/usr/bin/env python
#-*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

def to_xml(corpus) :
    root = ET.Element("corpus")
    root.set("debut", corpus.begin)
    root.set("fin", corpus.end)
    cat = ET.SubElement(root, "categories")
    for categorie in corpus.categories :
        ca = ET.SubElement(cat, "categorie")
        ca.text = categorie

    content = ET.SubElement(root, "content")
    for article in corpus.articles :

        a = ET.SubElement(content, "article")

        t = ET.SubElement(a, "title") 
        t.text = article.titre

        de = ET.SubElement(a, "description")
        de.text = article.description

        da = ET.SubElement(a, "date")
        da.text = article.date

        c = ET.SubElement(a, "categorie")
        c.text = article.categorie

        an = ET.SubElement(a, "analyse")

        for token in article.analyse :
            to = ET.SubElement(an, "token")
            to.set("form", token.forme)
            to.set("lemma", token.lemme)
            to.set("pos", token.pos)
            
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write(f"{corpus.begin}_{corpus.end}.xml", encoding="utf-8")
