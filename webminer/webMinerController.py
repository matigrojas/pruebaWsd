# -*- coding: utf-8 -*-
import threading, time, csv, operator
from optparse import OptionParser
import networkx as nx
from pattern.web import URL
#from progress import *
#from controller import *
#from search.testLinks import TestLinksClass #solo para hacer pruebas sin motor de busqueda
#from draw.twoDimensionalDrawing import *
#from algorithms.retrievalAlgorithms import *
from algorithmTools import QueryProcessor
from controller import *
from bd.consultasBD import *

class Structure:#es un clase auxiliar para encapsular una estructura.

    def  __init__(self,graph,domain):
        self.graph=graph
        self.domain=domain
    def getGraph(self):
        return self.graph
    def getDomain(self):
        return self.domain

class WebMinerController(object):

    #En todo momento trabaja con un unico objeto minePackage

    def __init__(self,cloudSize = 10,searchKey = "" ,id_request = 0, urls = [] , directorio = ""):
        super(WebMinerController, self).__init__()
        #self.progress=Process(id_request)
        self.minePackage=dict()
        self.searchKey=searchKey
        self.n=0
        self.directorio = directorio
        self.cloudSize=cloudSize
        #self.crawlerController=CrawlerController(directorio,id_request)
        self.crawlerController=CrawlerControllerPersistido(directorio,id_request)
        '''self.engineSearchController=EngineSearchController(self.progress)
        self.MEGA_CrawlerController=MEGA_CrawlerController(self.progress)
        self.IRController=InformationRetrievalController(self.progress)
        self.storageController=StorageController(self.progress)
        self.scraperController=ScraperController(self.progress)'''
        self.urls = urls
        self.id_request = id_request


    def run(self):
        self.minePackage['searchKey']=self.searchKey
        unProcessor = QueryProcessor()
        self.minePackage['searchKeyStemmer'] = unProcessor.processor(self.minePackage) #Se tokeniza la query (devuelve un diccionario de la manera {palabra: conteo} aplicando previamente el stemmer PORTER)
        self.minePackage['searchKey']=self.searchKey
        self.minePackage['cloudSize']=self.cloudSize #Setea un cludsize de 50
        self.minePackage['clouds']=self.startClouds(self.urls) #Clouds recibe una lista de objetos tipo estructura
        # clouds = self.minePackage['clouds']
        # for cloud in clouds:
        #     print cloud.graph.nodes()
        #     for n in cloud.graph.nodes():
        #         print n
        
        insertMinepackage(self.id_request,self.minePackage['searchKey'],self.minePackage['cloudSize']) #Persiste un nuevo MinePackage
        for cloud in self.minePackage['clouds']:
            insertCloud(self.id_request) #Persiste un cloud
            idCloud = dameUltimoCloud(self.id_request)[0][0] #Se obtiene el id del cloud recien creado
            for n in cloud.graph.nodes():
                insertNodoRaiz(idCloud,cloud.graph.node[n]['select'],cloud.graph.node[n]['weight_VSM'],cloud.graph.node[n]['weight_WA'],cloud.graph.node[n]['weight_OKAPI'],cloud.graph.node[n]['weight_SVM'],cloud.graph.node[n]['weight_CRANK'],cloud.graph.node[n]['totalScore'],cloud.graph.node[n]['link'])
        
        self.minePackage = None
        self.crawler() #Comienza Crawling
    
    def startClouds(self,urls):
        """
        statClouds: Recibe un conjunto de url's en la lista urls.

        Por cada URL Esta creando un grafo dirigido, ubicando como unico nodo, al que esta en n[0], para ello crea un objeto
        Structure, al cual se le añade el grafo dirigido de un elemento y el dominio de la url, obtenido por url.domain
        """
        clouds=list()
        for n in urls: #Recorre cada url presente en urls (urls es una lista en la que cada url es a su vez una lista)
            url=URL(n[0]) #Crea un objeto pattern.URL, enviando la url contenida en la posicion 0 de n
            graph=nx.DiGraph() #Inicializa un grafo dirigido (Apunta a uno nodo en especifico) vacio (permite auto apuntado)
            graph.add_node(str(n[0]),
                        select=True,
                        ID=0,
                        weight_VSM=0.0,
                        weight_WA=0.0,
                        weight_OKAPI=0.0,
                        weight_SVM=0.0,
                        weight_CRANK=0.0,
                        totalScore=0.0,
                        link=n[0],
                        methodData=None,
                        )
            clouds.append(Structure(graph,url.domain)) #Crea un objeto Structure
        return clouds

    def crawler(self):
        self.crawlerController.start()