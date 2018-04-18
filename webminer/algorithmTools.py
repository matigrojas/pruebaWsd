# -*- coding: utf-8 -*-
from pattern.en import parse, Sentence
from pattern.vector import stem, PORTER, LEMMA, count, words, Vector, distance, Document, Model, TFIDF

class QueryProcessor:
    def __init__(self):
        pass
    def processor(self,minePackage):
        print '####SEARCH_KEY:',minePackage['searchKey']
        s = Sentence(parse(minePackage['searchKey']))
        minePackage['searchKey']=count(words(s), stemmer=PORTER) #Retorna diccionario {palabra: cantidad}
        return minePackage['searchKey']
