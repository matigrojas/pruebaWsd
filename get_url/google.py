# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import os, sys, unicodedata ; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.web import Google, plaintext, URL, SEARCH
from HTMLParser import HTMLParser

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def generar_consulta_google(q):
    url = []
    reload(sys)
    sys.setdefaultencoding('utf8')

    # engine_google = Google(license="AIzaSyCvvHb8SYgHvS5gEIQabxuJ0Kl0sYdHl9U", language="en")
    engine_google = Google(license="AIzaSyCKlCEJ41mE_6gqTN2AI9J4iSB-2L55zR0", language="en")
    for consulta in q:
        for i in range(1, 2):
            for result in engine_google.search(consulta, start=i, count=10, type=SEARCH, cached=False):

                titulo = strip_accents(result.title)
                url.append(result.url)
    return url
