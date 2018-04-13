from interfaz import proyecto
from google import *
from bing import *

def dame_urls(proyecto):
    proyecto.urls_google = generar_consulta_google(proyecto.consultas)#Obtiene URLS de GOOGLE
    proyecto.urls_bing = generar_consulta_bing(proyecto.consultas)#Obtiene URLS de BING
    print proyecto.urls_bing

