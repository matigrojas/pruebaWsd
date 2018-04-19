import math

class BM25:
 
    def __init__(self):
        pass
 
    def run(self,minePackage):
        k=2.0
        #k=1.2
        b=0.75
        score=float()
        query=minePackage['searchKey']
        print 'searchKey:', query
        clouds=minePackage['clouds']
        scoreList=dict() 
        all_documents=self.docList(minePackage)
        N=len(all_documents)
        avgdl_docs=self.avgdl(all_documents)#logitud promedio de los documentos
        for cloud in clouds:
            for n in cloud.graph.nodes():
                okapiScore=0.0
                for qi in query:
                    nqi=self.n_qi(qi,all_documents)#Obtengo el numero de documentos que contienen la palabra clave qi
                    IDF=self.idf_qi(N,nqi)#calculo IDF segun el metodo OKAPI-BM25
                    fqi_d=float(self.freq_qi_doc(qi,all_documents[n]))#frecuencia de aparicion de una qi en el documento analizado
                    length=float(self.document_length(all_documents[n]))#se determina la logitud total del documento
                    score=self.score(IDF,fqi_d,length,avgdl_docs,k,b)#Puntuacion para un documento doc
                    okapiScore+=IDF*score
                cloud.graph.node[n]['weight_OKAPI']=okapiScore
 
    def score(self,IDF,fqi_d,length,avgdl,k,b):
        score=float()
        score=(fqi_d*(k+1))/(fqi_d+k*(1-b+(b*(length/avgdl))))
        #print '*'*100
        #print 'fqi_d:',fqi_d
        #print 'length:',length
        #print 'avgdl:',avgdl
        #print 'k:',k
        #print 'b:',b
        #print 'SCORE: ',score
        #print '*'*100
        return score
 
    def idf_qi(self,N,nqi): #es el peso IDF de las palabras claves que aparece en la consulta
        idf=math.log((N-nqi+0.5)/(nqi+0.5),math.exp(1))
        #print '*'*100
        #print 'N:',N
        #print 'nqi:',nqi
        #print 'IDF: ',idf
        #print '*'*100
        return idf
 
    def document_length(self,doc):
        length=0
        for term in doc:
            length+=int(doc[term])
        return length

    def freq_qi_doc(self,qi,doc):
        fqi_doc=0
        if qi in doc:
            fqi_doc=doc[qi]
        return fqi_doc

    def avgdl(self,all_documents):
        total_terms=0
        N=len(all_documents)
        for doc in all_documents:
            document=all_documents[doc]
            for term in document:
                total_terms+=document[term]
        avgdl=float(total_terms)/float(N)
        #print '#####AVGDL: '
        #print 'avgdl:', avgdl
        #print 'total palabras: ',total_terms
        #print 'N: ',N
        return avgdl

    def n_qi(self,qi,all_documents): #cantidad de documentos que tienen la palabra clave qi
        nqi=0
        for doc in all_documents:
            document=all_documents[doc]
            if qi in document:
                nqi+=1
        return nqi

    def docList(self,minePackage):
        clouds=minePackage['clouds']
        documents=dict()
        for cloud in clouds:
            for n in cloud.graph.nodes():
                nodo=cloud.graph.node[n]['methodData']
                link=cloud.graph.node[n]['link']
                documents[link]=nodo.getData()
        return documents

