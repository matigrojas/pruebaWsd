#-*- coding: utf-8 -*-

from interfaz import proyecto
from google import *
from bing import *
from msxmlExcite import *
from intelligo import *

def dame_urls(proyecto):
    #Obtención links GOOGLE
    try:
        proyecto.urls_google = generar_consulta_google(proyecto.consultas)#Obtiene URLS de GOOGLE
    except:
        print "Exception: GOOGLE"
        pass
    
    #Obtención links bing
    try:
        proyecto.urls_bing = generar_consulta_bing(proyecto.consultas)#Obtiene URLS de BING
    except:
        print "Exception: BING"
        pass
    
    #Obtención links excite
    try:
        proyecto.urls_excite = generar_consulta_excite(proyecto.consultas)#Obtiene URLS de EXCITE
    except:
        print "Exception: EXCITE"
        pass
    
    #Obtención Links Intelligo
    try:
        proyecto.urls_inteligo = generar_consulta_intelligo(proyecto.consultas) #Obtiene Consultas INTELLIGO
    except:
        print "Exception: INTELLIGO"
        pass

