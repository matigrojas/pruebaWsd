from interfaz import proyecto
from google import *
from bing import *
from msxmlExcite import *

def dame_urls(proyecto):
    proyecto.urls_google = generar_consulta_google(proyecto.consultas)#Obtiene URLS de GOOGLE
    proyecto.urls_bing = generar_consulta_bing(proyecto.consultas)#Obtiene URLS de BING
    proyecto.urls_excite = generar_consulta_excite(proyecto.consultas)#Obtiene URLS de EXCITE
    print proyecto.urls_bing

