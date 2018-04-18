#-*- coding: utf-8 -*-

from interfaz import proyecto

def webminer_main(proyecto):
    consultas = ''
    for clave in proyecto.consultas:
        consultas += clave 
    print consultas