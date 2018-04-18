from interfaz import proyecto
from google import *
from bing import *
from msxmlExcite import *
from intelligo import *

def dame_urls(proyecto):
    proyecto.urls_google = generar_consulta_google(proyecto.consultas)#Obtiene URLS de GOOGLE
    proyecto.urls_bing = generar_consulta_bing(proyecto.consultas)#Obtiene URLS de BING
    proyecto.urls_excite = generar_consulta_excite(proyecto.consultas)#Obtiene URLS de EXCITE
    proyecto.urls_inteligo = generar_consulta_intelligo(proyecto.consultas) #Obtiene Consultas INTELLIGO
    print "URLS INTELLIGO"
    print proyecto.urls_inteligo
    print 

