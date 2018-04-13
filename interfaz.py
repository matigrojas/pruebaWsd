#-*- coding: utf-8 -*-
from get_url.controladora import dame_urls

class proyecto:
    def __init__(self,id_proy, titulo_proy, consultas, directorio):
        self.id_proyecto = id_proy
        self.titulo_proyecto = titulo_proy
        self.consultas = consultas
        self.directorio = directorio 
        self.urls_google = list()
        self.urls_bing = list()
        self.urls_inteligo = list()
        self.urls_excite = list()



if __name__ == '__main__':
    #Se comienza con la lectura de datos necesarios
    id_proyecto = raw_input('Ingrese el numero de proyecto: ').lower()
    #Titulo del proyecto
    titulo_proyecto = raw_input('Ingrese el Titulo del proyecto: ').lower()
    #Consulta (se van a ingresar las consultas que se deseen hacer a mano!)
    consultas = list()
    consulta = raw_input('Ingrese una consulta (Para dejar de cargar presione 0): \n').lower()
    while (consulta != '0'):
        consultas.append(consulta)
        consulta = raw_input('Ingrese una consulta (Para dejar de cargar presione 0): \n')
    #Armado de directorio
    usuario = raw_input('Ingrese su usuario: ').lower()
    directorio = usuario+ '/' + '000'+id_proyecto
    #Creacion de proyecto
    proyecto = proyecto(id_proyecto,titulo_proyecto,consultas,directorio)
    dame_urls(proyecto)
