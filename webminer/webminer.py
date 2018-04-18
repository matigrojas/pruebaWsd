#-*- coding: utf-8 -*-

from webMinerController import WebMinerController

def webminer_main(proyecto):
    consulta = '' #Consulta final
    agregadas = list()
    no_deseadas = ['and','or','not','paper'] #faltan eliminar otras palabras no deseadas
    #Armado de consulta general eliminando palabras no deseadas
    for clave in proyecto.consultas:
        clave = clave.lower()
        clave = clave.split()
        for pal in clave:
            if((pal not in agregadas) and (pal not in no_deseadas)):
                agregadas.append(pal)
                consulta += pal + " "
    #Armado de lista, de listas de urls filtradas, formato necesario para pattern crawl
    url_para_cloud = list()
    for url,puntaje in proyecto.urls_filtradas:
        aux_url = []
        aux_url.append(url)
        url_para_cloud.append(aux_url) 
    
    controlador_webminer = WebMinerController(searchKey=consulta,id_request=proyecto.id_proyecto,urls=url_para_cloud,directorio=proyecto.directorio)
    controlador_webminer.run()