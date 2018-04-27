#import time
# -*- coding: utf-8 -*-
from tools.algorithmTools import * #Herramientas de calculo para algoritmo booleando y modelo espacio vectorial
from tools.okapiTools.okapi import * #Heramientas de calculo para algoritmo okapi
from tools.crankTools.crank import * #Heramientas de calculo para algoritmo Crank
#from tools.svmTools.svm import * #Herramientas de calculo para algoritmo basado en maquinas de vectores de soporte
#from tools.lsaTools.lsa import * #Herramientas de calculo para algoritmo de analisis semantico latente

#Inicio
class Algorithm(object):

    name=str()
    tokens=None

    def __init__(self,name):
        super(Algorithm,self).__init__()
        self.name = name

    def tokenizer(self,minePackage):
        tokens=Tokenizer()
        tokens.run(minePackage)

    def queryProcessor(self):
        processor=QueryProcessor()
        return processor
        #processor.processor(minePackage)

    def distanceVector(self):
        distance=DistanceVector()
        return distance

    def getName(self):
        return self.name

    def vectorSim(self):
        return VectorSimilarity()

    def weighting(self):
        return WeightingProccess()

    def okapi_BM25(self):
        return BM25()

    def totalScores(self,minePackage):
        clouds=minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                cloud.graph.node[n]['totalScore']=(cloud.graph.node[n]['weight_VSM']+cloud.graph.node[n]['weight_WA']+cloud.graph.node[n]['weight_OKAPI'])/3

    def ranking(self,minePackage):
        clouds=minePackage['clouds']
        weightedList=dict()
        self.totalScores(minePackage)
        for cloud in clouds:
            for n in cloud.graph.nodes():
                scores=list()
                scores.append(cloud.graph.node[n]['weight_VSM'])
                scores.append(cloud.graph.node[n]['weight_WA'])
                scores.append(cloud.graph.node[n]['weight_OKAPI'])
                scores.append(cloud.graph.node[n]['weight_CRANK'])
                scores.append(cloud.graph.node[n]['totalScore'])
                weightedList[cloud.graph.node[n]['link']]=scores
            self.printRanking(weightedList)

    def printRanking(self,weightedList):
        print
        print 'INFORMATION RETRIEVAL ALGORITHM: Vector Space Model && Weighted Approach && OKAPI-BM25'
        print
        print 'Ranking:'
        print
        ranking=sorted(weightedList.items(),key = lambda x:x[1][3])
        i=len(ranking)-1
        elem=-1
        f=1
        while i>=0:
            print '-'*100
            print f,'|||',ranking[elem][0],'|||','TOTAL SCORE:',ranking[elem][1][3]
            print '  VSM:',ranking[elem][1][0]
            print '   WA:',ranking[elem][1][1]
            print 'OKAPI:',ranking[elem][1][2]
            print 'CRANK:', ranking[elem][1][3]
            #print f,'|||',ranking[elem][0],'|||',ranking[elem][1][0],'|||',ranking[elem][1][1],'|||',ranking[elem][1][2],'|||',ranking[elem][1][3] #imprime en orden descendente
            elem-=1
            i-=1
            f+=1
        print

    def crank_Scoring(self):
        return CRanking()

    def __str__(self):
        return self.name



'''#### Booleano ################################################################'''
class Boolean(Algorithm):

    def __init__(self,name):
        super(Boolean,self).__init__(name)

    def run(self,minePackage):
        self.tokenizer(minePackage)
        self.booleanFilter(minePackage)

    def booleanFilter(self,minePackage):
        relevant=[]
        notRelevant=[]
        clouds=minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                methodData=cloud.graph.node[n]['methodData']
                document=methodData.getData()
                if ( (('analysi' in document)and('pattern' in document)and('googl' in document)) and ('coock' in document)):
                    relevant.append(cloud.graph.node[n]['link'])
                else:
                    notRelevant.append(cloud.graph.node[n]['link'])
        print 'INFORMATION RETRIEVAL ALGORITHM: Boolean method'
        print
        print 'Relevant links:'
        for rel in relevant:
            print rel
        print 'Total:',len(relevant)
        print
        print 'Not relevant links:'
        for nrel in notRelevant:
            print nrel
        print 'Total:',len(notRelevant)



'''#### Booleano Extendido #####################################################'''
class ExtendedBoolean(Algorithm):

    def __init__(self,name):
        super(ExtendedBoolean,self).__init__(name)

    def run(self,minePackage):
        self.tokenizer(minePackage)
        self.booleanFilter(minePackage)

    def booleanFilter(self,minePackage):
        weightedList={}
        query='python','support','express','sign','zero','mathemat','ceil'
        clouds=minePackage['clouds']
        for cloud in clouds:
            for n in cloud.graph.nodes():
                methodData=cloud.graph.node[n]['methodData']
                document=methodData.getData()
                #print len(document)
                weightedList[cloud.graph.node[n]['link']]=self.extendedOperator(document,query)
        self.booleanRanking(weightedList)

    def extendedOperator(self,document,query):
        tf=[]
        for w in query:
            if w in document:
                tf.append(document[w])
            else:
                tf.append(0)
        return tf[0]*tf[1]*tf[2]+(tf[3]+tf[4]+tf[5]+tf[6])

    def booleanRanking(self,weightedList):
        print 'INFORMATION RETRIEVAL ALGORITHM: Extended boolean method'
        print
        print 'Ranking:'
        print
        ranking=sorted(weightedList.items(),key = lambda x:x[1])
        #Orden Descendente:
        i=len(ranking)-1
        elem=-1
        f=1
        while i>=0:
            print f,'|||',ranking[elem][0],'||| W=',ranking[elem][1]
            elem-=1
            i-=1
            f+=1



'''#### Modelo de espacio vectorial #####################################################'''
class VectorSpaceModel(Algorithm):
    def __init__(self,name):
        super(VectorSpaceModel,self).__init__(name)
    def run(self,minePackage):#recibe como parametro una referencia de la clase progress
        weightedList={}
        #query=minePackage['searchKey']
        vectorSimilarity=self.vectorSim() #Crea el objeto de VSM
        vectorSimilarity.calculate(minePackage) #Calcula VSM y Lo setea en el CLOUD
        #self.ranking(minePackage,progress)

'''#### Documento Vector #################################################################'''
class DocumentVector(Algorithm):
    def __init__(self,name):
        super(DocumentVector,self).__init__(name)
    def run(self,minePackage):
        weightedList={}
        self.tokenizer(minePackage)
        processor=self.queryProcessor()
        processor.processor(minePackage)
        distance=self.distanceVector()
        distance.run(minePackage)
        #self.ranking(minePackage,progress)

'''#### Enfoque Ponderado ################################################################'''
class WeightedApproach(Algorithm):
    def __init__(self,name):
        super(WeightedApproach,self).__init__(name)
    def run(self,minePackage):
        #weightedList={}
        # self.tokenizer(minePackage)#Descarga contenido y lo tokeniza
        # processor=self.queryProcessor()#Se instancia un procesador de query
        weightingProccess=self.weighting()#Se instancia la clase encargada de ponderar contenido de los nodos
        weightingProccess.run(minePackage)#Se inicia proceso de ponderacion de nodos y lo setea en el cloud
        #self.ranking(minePackage,progress)#Se realiza el proceso de ranking

'''#### Okapi BM25 ########################################################################'''
class Okapi(Algorithm):
    def __init__(self,name):
        super(Okapi,self).__init__(name)
    def run(self,minePackage):
        #weightedList={}
        #self.tokenizer(minePackage) #Descarga contenido y lo tokeniza
        #processor=self.queryProcessor() #Se instancia un procesador de query
        #processor.processor(minePackage) #Se tokeniza la query
        score=self.okapi_BM25() #se instancia el modelo BM25
        score.run(minePackage) #se ejecuta el calculo de Okapi score(D,Q) y lo setea en el cloud
        # self.ranking(minePackage,progress) # se realiza el proceso de ranking

'''
FUNCIONAMIENTO:
-hallar frecuencia de aparicion en el documento, de los terminos que aparecen en la consulta: f(qi,D)
-longitud del documento en numero de palabras: |D|
-hallar longitud promedio de los documentos sobre los cuales se aplica el algoritmo: avgdl
-hallar numero total de documentos en la coleccion: N
-hallar el numero de documentos que contienen la palabra clave qi: n(qi)
-calcular el IDF de las palabras de la query: IDF(qi)=log((N-n(qi)+0.5)/(n(qi)+0.5))
-fijar constante empirica k1=1.2 - 2.0
-fijar constante empirica b=0.75
-Hallar score okapiBM25: score(D,Q)= sum(IDF(qi)* (f(qi,D)*k1+1/f(qi,d)+k1*(1-b+b*(|D|/avgdl))))
'''

'''#### Ranking Colaborativo ######################################################'''
class CRank(Algorithm):
    def __init__(self,name):
        super(CRank,self).__init__(name)
    def run(self,minePackage):
        print 'AHORA SE HACE EL CRANK::'
        #self.tokenizer(minePackage) #Descarga contenido y lo tokeniza
        #processor=self.queryProcessor() #Se instancia un procesador de query
        #processor.processor(minePackage) #Se tokeniza la query
        rankingColaborativo=self.crank_Scoring()#se instancia el modelo de recuperacion CRANK
        rankingColaborativo.run(minePackage) #se ejecuta el calculo de Okapi score(D,Q) y lo setea en el cloud
        #self.ranking(minePackage) # se realiza el proceso de ranking
        self.totalScores(minePackage)

'''#### Support Vector Machine ####################################################'''
class SupportVectorMachine(Algorithm):
    def __init__(self,name):
        super(SupportVectorMachine,self).__init__(name)
    def run(self,minePackage):
        pass

'''#### Latent Semantic Analysis ##################################################'''
class LatentSemanticAnalysis(Algorithm):
    def __init__(self,name):
        super(LatentSemanticAnalysis,self).__init__(name)
    def run(self,minePackage):
        pass
