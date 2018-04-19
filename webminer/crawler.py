import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import random
import networkx as nx
from tools import *
from pattern.web import Crawler, find_urls, DEPTH, BREADTH,URL, MIMETYPE_PDF, FIFO, LIFO

class Structure:#es un clase auxiliar para encapsular una estructura.

    graph=nx.DiGraph()
    domain=str()
    termsDocGraph=None
    weightedQuery=None

    def  __init__(self,graph,domain):
        self.graph=graph
        self.domain=domain

    def getDomain(self):
        return self.domain
    def setTermsDocGraph(self,value):
        self.termsDocGraph=value
    def getTermsDocGraph(self):
        return self.termsDocGraph
    def setWeightedQuery(self,value):
        self.weightedQuery=value
    def getWeightedQuery(self):
        return self.weightedQuery



class SimpleCrawler1(Crawler):
    count=1
    social=0
    newRoad=None
    structure=nx.DiGraph()
    badLink=Filter()

    def visit(self, link, source=None):
        linkReferrer=link.referrer
        linkUrl=link.url
        if '#' in link.url: #Toma el enlace principal, no la extension post #
            part=link.url.partition('#') 
            linkUrl=unicode(part[0])
        if '#' in link.referrer:
            partRef=link.referrer.partition('#')
            linkReferrer=unicode(partRef[0])
        if linkUrl in self.structure.nodes():
            pass #Si ya existe un nodo con esa URL, pasa
        else:
            print str(self.count)," VISITING:", linkUrl, " <----- FROM:", linkReferrer
            self.structure.add_node(linkUrl,
                                    select=True,
                                    ID=0,
                                    weight_VSM=0.0,
                                    weight_WA=0.0,
                                    weight_OKAPI=0.0,
                                    weight_SVM=0.0,
                                    weight_CRANK=0.0,
                                    totalScore=0.0,
                                    link=linkUrl,
                                    methodData=None)
            self.count+=1 
            if linkReferrer!='':
                self.structure.node[linkReferrer]['select']=False
                self.structure.add_edge(linkReferrer,linkUrl)

    def fail(self, link):
        url=URL(link.url)
        pdf=url.mimetype in MIMETYPE_PDF
        if pdf:
            print str(self.count)," VISITING:", link.url, " <----- FROM:", link.referrer
            self.structure.add_node(link.url,
                                    select=False,
                                    ID=0,
                                    weight_VSM=0.0,
                                    weight_WA=0.0,
                                    weight_OKAPI=0.0,
                                    weight_SVM=0.0,
                                    weight_CRANK=0.0,
                                    totalScore=0.0,
                                    link=link.url,
                                    methodData=None)
            if link.referrer!='':
                self.structure.node[link.referrer]['select']=False
                self.structure.add_edge(link.referrer,link.url)
            self.count+=1
        else:
            print "failed: ", link.url
            if link.url in self.structure.nodes():
                self.structure.remove_node(link.url)

#    def priority(self, link, method=DEPTH):
#        #if "linkedin" in link.url or "twitter" in link.url or "facebook" in link.url or "google" in link.url:
#        if self.badLink.detect(link.url):
#            return 0.0
#        else:
#            return Crawler.priority(self, link, method)

    def newStructure(self,graph):
        self.structure=graph
    
    def getStructure(self):
        return self.structure