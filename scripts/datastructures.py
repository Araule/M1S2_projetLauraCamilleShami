#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    forme: str
    lemme: str
    pos: str

@dataclass
class Article:
    titre: str
    description: str
    date: str
    categorie: str
    analyse: List[Token]

@dataclass
class Corpus:
    categories: List[str]
    begin: str
    end: str
    chemin: Path
    articles: List[Article]