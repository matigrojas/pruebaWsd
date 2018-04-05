#-*- coding: utf-8 -*-
from pattern.web import Wikipedia
from pattern.en import parse,pprint
from nltk.corpus import wordnet as wn

"""
definicion_en_wiki(conc): encuentra la definicion correspondiente al termino conc.
"""
def definicion_en_wiki(conc):
    wiki_result = Wikipedia().search(conc)
    return wiki_result

"""
encontrar_sustantivos_compuestos(rp): busca encontrar aquellos sustantivos, adjetivos o verbos compuestos cuyo significado
sea mas relevante si ambas se encuentran juntos a que si están separados. rp es un conjunto de palabras tokenizadas. 
"""
def encontrar_sustantivos_compuestos(rp):
    i = 0
    cadena = []
    unidos = []
    while i < (len(rp)-1):
        if(((str(rp[i][1]).startswith('J')) or (str(rp[i][1]).startswith('V')) or (str(rp[i][1]).startswith('N'))) and ((str(rp[i+1][1]).startswith('J')) or (str(rp[i+1][1]).startswith('V')) or (str(rp[i+1][1]).startswith('N')))):
            conc = rp[i][0] + ' ' + rp[i+1][0]
            if(definicion_en_wiki(conc)!= None):
                cadena.append(conc)
                unidos.append(rp[i][0])
                unidos.append(rp[i+1][0])
            else:
                if (i+1!=len(rp)-2):
                    cadena.append(rp[i][0])
                else:    
                    cadena.append(rp[i][0])
                    cadena.append(rp[i+1][0])
        else:
            if(rp[i][0] not in unidos):
                cadena.append(rp[i][0])
            if (i+1==len(rp)-1):
                cadena.append(rp[i+1][0])
        i+=1
    print cadena
    return cadena

"""
 busca_wiki(sent): obtiene un corpus correspondiente a una posicion en la tabla, cuya extension sea de dos terminos,
 lo cual significa que esos terminos juntos poseen significado propio, resultando diferente a su consideracion por 
 separado.
"""
#TODO: Recorrer algunos articulos relacionados por cada palabra (principalmente los del articulo principal)
def busca_wiki(sent):
    wiki_result = definicion_en_wiki(sent)
    seccion_principal = []
    sectores_no_deseados = [u'See also',u'References',u'Sources']
    #Acceder solo a la definicion principal, si esta disponible el articulo
    if(wiki_result!=None):
        for x in wiki_result.sections:
            if x.title == wiki_result.title:
                seccion_principal.append(x.string)
                print x.links
    return seccion_principal

"""TODO: Metodo modificado de LESK (pudiendo ser el simple, el original o el ampliado/extendido (se modifica de PYWSD))
se lo va a utilizar para determinar los demas sentidos una vez obtenido el principal"""

"""TODO: Metodo de pattern_lsa utilizado para a partir del corpus obtenido de wikipedia, obtener el sentido correcto de
las palabras conformantes"""

"""TODO: Metodo de obtencion de definiciones (glosses) por cada synset (Ya desarrollado en otro codigo controladora.py)"""

if __name__ == '__main__':
    sent2 = 'tea added value manufacture'
    result_parse = parse(sent2).split()
    sust_comp = encontrar_sustantivos_compuestos(result_parse[0])
    for x in sust_comp:
        if len(x.split())>1:
            if len(wn.synsets(x))>0:
                """TODO: si existe en wordnet no es necesaria una busqueda en wikipedia, por lo tanto, se opera como si fuera un
                termino comun"""
                print wn.synsets(x)
            else:
                """
                TODO: si no existe en wordnet, se busca en wikipedia y se utiliza otro metodo de desambiguacion de sentido de la palabra
                """    
                print busca_wiki(x)
        

