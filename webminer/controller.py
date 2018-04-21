# -*- coding: utf-8 -*- 
#from webCrawler.crawler_07 import *
#from webCrawler.crawler_08 import *
#from webScraper.scraper import *
from pattern.web import URL
from crawler import *
from algorithms.retrievalAlgorithms import *
from algorithms.tools.algorithmTools import MethodData

class Controller(object):
    def __init__(self):
        super(Controller,self).__init__()

class CrawlerController(Controller):

    def __init__(self,directorio,id_request):
        super(CrawlerController,self)
        self.IRController=InformationRetrievalController()
        self.stop=False
        self.directorio = directorio
        self.id_request = id_request

    def trueNodesSelection(self,cloud):
        in_true=list()
        for n in cloud.graph.nodes(): #Recorre los nodos del graph, que es un atributo de Structure
            nod=cloud.graph.node[n] #Obtiene el nodo n
            if nod['select']==True: #Al principio siempre es true, si es verdadero lo añade a in_true
                in_true.append(n)
        return in_true

    def start(self,minePackage):
        cloudSize = minePackage['cloudSize'] #Setea la cantidad de nodos por nivel
        searchKey = minePackage['searchKey'] #Setea la clave de busqueda
        step = 0
        while step<10: #Mas adelante setear get_stop; esto indica la cantidad de niveles
            clouds = minePackage['clouds']
            for cloud in clouds:
                true_nodes = self.trueNodesSelection(cloud)
                for n in true_nodes:
                    cloud.graph.node[n]['select'] = False
                    crawler = SimpleCrawler1 (n,delay=0.1)
                    crawler.newStructure(cloud.graph)
                    time = 0
                    while len(crawler.visited)<cloudSize:
                        print 'Explorando ...'
                        try:
                            crawler.crawl(method=DEPTH)
                        except:
                            print "ERROR EN CRAWL: se continua con el proceso"
                            break
                        time+=1
                        if time>cloudSize*10:
                            break
                    print 
                    print '#####Generando documentos#####'
                    self.IRController.start(minePackage) #Recupera Informacion
            step += 1 #Controla los niveles a expandir, en este caso 10
        #FALTA SCRAPPER CONTROLLER
        print "Proceso Finalizado"


                    
class InformationRetrievalController(Controller):

    def __init__(self,):
        super(InformationRetrievalController,self).__init__()

    def start(self,minePackage):
        self.descargarContenido(minePackage)
        pattern_methods=[VectorSpaceModel('Vector Space Model')]
        own_methods=[WeightedApproach('Weighted Approach'),Okapi('Okapi-BM25'),CRank('CRank')]
        for algorithm in pattern_methods:
            algorithm.run(minePackage) #Ejecuta algoritmos propios de Pattern, en este caso VSM.

        for algorithm in own_methods:
            algorithm.run(minePackage) #Ejecuta algoritmos de la tesis.

    def descargarContenido(self,minePackage):
        """agrega al cloud un objeto denominado methodData, el cual va a tener la URL y el contenido de esa URL"""
        clouds = minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                if(cloud.graph.node[n]['methodData']==None):
                    unMethodData = MethodData("",cloud.graph.node[n]['link']) #El contenido se añade cuando se crea el objeto
                    cloud.graph.node[n]['methodData'] = unMethodData #Method Data va a tener el contenido de la url pasada

