# -*- coding: utf-8 -*- 
#from webCrawler.crawler_07 import *
#from webCrawler.crawler_08 import *
#from webScraper.scraper import *
from pympler import asizeof 
from pattern.web import URL
from pattern.en import parse, Sentence
from pattern.vector import stem, PORTER, LEMMA, count, words, Vector, distance, Document, Model, TFIDF
from crawler import *
from algorithms.retrievalAlgorithms import *
from algorithms.tools.algorithmTools import MethodData
from bd.consultasBD import *
import gc

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
        print "peso inicial minePackage: " + str(asizeof.asizeof(minePackage)) + 'bytes'
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
                        crawler.crawl(method=None)
                        time+=1
                        if time>cloudSize*10:
                            break
                    print 
                    print '#####Generando documentos#####'
                    print "Peso Actual: " + str(asizeof.asizeof(minePackage)) + 'bytes'
                    self.IRController.start(minePackage) #Recupera Informacion
                    print "Nivel nro: " + str(step)
            step += 1 #Controla los niveles a expandir, en este caso 10
        #FALTA SCRAPPER CONTROLLER
        print "Proceso Finalizado"

class CrawlerControllerPersistido(Controller):

    def __init__(self,directorio,id_request):
        super(CrawlerControllerPersistido,self)
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

    def start(self):
        cloudSize = dameCloudSize(self.id_request)
        cloudSize = cloudSize[0][0]
        searchKey = dameSerchKey(self.id_request)
        searchKey = searchKey[0][0]
        step = 0
        while step<=5: #Mas adelante setear get_stop; esto indica la cantidad de niveles 
            for id_cloud in dameIdCloud(self.id_request): #Obtiene IDS de los clouds que pertenecen al proyecto
                print "Id Cloud: " + str(id_cloud[0])
                cloud = self.generar_cloud(dameNodo(id_cloud[0]))
                true_nodes = self.trueNodesSelection(cloud)
                for n in true_nodes:
                    try:
                        cloud.graph.node[n]['select'] = False
                        crawler = SimpleCrawler1 (n,delay=0.1)
                        crawler.newStructure(cloud.graph)
                        time = 0
                    except:
                        continue    
                    while len(crawler.visited)<cloudSize:
                        print "Cloudsize = " + str(cloudSize) + " Crawler Visited = " + str (len(crawler.visited)) + " Nivel =  " + str(step)
                        print 'Explorando ...'
                        crawler.crawl(method=None)
                        time+=1
                        if time>cloudSize*10:
                            break
                    actualizarSelect(cloud.graph.node[n]['ID'],cloud.graph.node[n]['select'])
                    print 
                    print '#####Generando documentos#####'
                    #Creacion de minePackage
                    clouds = list()
                    clouds.append(cloud)
                    minePackage = dict()
                    minePackage['clouds'] = clouds
                    minePackage['searchKey'] = searchKey
                    minePackage['searchKeyStemmer'] = count(words(Sentence(parse(searchKey))), stemmer=PORTER)
                    self.IRController.start(minePackage) #Recupera Informacion
                    #FALTA SCRAPPER CONTROLLER
                #Se pone none para que no ocupen espacio innecesario, todo ya fue guardado en BD
                minePackage = None
                cloud = None
                gc.collect    
            step += 1
            print "Explorando nivel nro: " + str(step)
            #Controla los niveles a expandir, en este caso 10
        print "Proceso Finalizado"

    def generar_cloud(self,nodo):
        url = URL(nodo[0][9])
        graph=nx.DiGraph() #Inicializa un grafo dirigido (Apunta a uno nodo en especifico) vacio (permite auto apuntado)
        for nodos in nodo:
            graph.add_node(nodos[9],
                        select=nodos[2],
                        ID=nodos[0],
                        weight_VSM=nodos[3],
                        weight_WA=nodos[4],
                        weight_OKAPI=nodos[5],
                        weight_SVM=nodos[6],
                        weight_CRANK=nodos[7],
                        totalScore=nodos[8],
                        link=nodos[9],
                        methodData=None,
                        )
            if(nodos[10]!=None):
                linkReferrer = dame_url_nodo_padre(nodos[10])
                graph.add_edge(linkReferrer,nodos[9]) #Crea un enlace entre ambos nodos
        return Structure(graph,url.domain)
        """ES NECESARIO CREAR LOS BORDES EDGES; PARA RELACIONAR NODOS!!!!!!!"""

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
        
        #Se Persisten los datos del ranking
        for cloud in minePackage['clouds']:
            for n in cloud.graph.nodes():
                actualizarPesoNodo(cloud.graph.node[n]['ID'],cloud.graph.node[n]['weight_VSM'],cloud.graph.node[n]['weight_WA'],cloud.graph.node[n]['weight_OKAPI'],cloud.graph.node[n]['weight_SVM'],cloud.graph.node[n]['weight_CRANK'],cloud.graph.node[n]['totalScore'])

    def descargarContenido(self,minePackage):
        """agrega al cloud un objeto denominado methodData, el cual va a tener la URL y el contenido de esa URL"""
        clouds = minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                if(cloud.graph.node[n]['methodData']==None):
                    md = obtenerMethodData(cloud.graph.node[n]['ID'])
                    if(len(md)>0):
                        print "Entró"
                        unMethodData = MethodData("",contenidoBd=md[0][0])
                        cloud.graph.node[n]['methodData'] = unMethodData
                    else:    
                        unMethodData = MethodData("",cloud.graph.node[n]['link']) #El contenido se añade cuando se crea el objeto
                        cloud.graph.node[n]['methodData'] = unMethodData #Method Data va a tener el contenido de la url pasada
                        insertMethodData(self.mejorarContenido(unMethodData.contenido),cloud.graph.node[n]['ID']) #Persiste MethodData

    def mejorarContenido (self, cont):
        miCont = cont.encode('utf-8',errors='replace')
        miCont = miCont.replace("\'","\\\'")
        return miCont