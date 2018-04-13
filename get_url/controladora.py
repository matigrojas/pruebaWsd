from interfaz.proyecto import *
from google import *

def dame_urls(proyecto):
    proyecto.urls_google = generar_consulta_google(proyecto.consultas)
    print urls_google

