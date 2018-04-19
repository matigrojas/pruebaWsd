from pattern.vector import *
class CRanking:

    def __init__(self):
        self.levels=list()
        self.back=3


    def run(self,minePackage):
        clouds=minePackage['clouds']
        query = minePackage['searchKeyStemmer']
        unaListaDocumentos = []
        unaListaModel = []
        for cloud in clouds:
            for n in cloud.graph.nodes():
                content = cloud.graph.node[n]['methodData'].getContent()

                unDocumento = DocumentoCrank()
                unDocumento.url = cloud.graph.node[n]['link']
                unDocumento.contenido = content
                unDocumento.pattern = Document(content, stemmer = PORTER, name=unDocumento.url)
                # unDocumento.score = self.calcular_score_relevance_crank(unDocumento,query)
                unaListaDocumentos.append(unDocumento)
                unaListaModel.append(unDocumento.pattern)

        model = Model(documents=unaListaModel, weight=TFIDF)

        for unDocumento in unaListaDocumentos:
            unDocumento.score = self.calcular_score_relevance_crank(unDocumento,query,model)
        for cloud in clouds:
            self.levels=list()
            for n in cloud.graph.nodes():
                # print '#'*50
                # print 'Nodo: ',n
                self.backLinks(cloud,n,0)
                # print 'LEVELS:'
                # print '-'*50

                auxiliarBackLinks = list()
                for level in self.levels:
                    for link in level:
                        auxiliarBackLinks.append(link)

                unDocumentBack = None
                unDocumento = next((x for x in unaListaDocumentos if x.url == n), None)
                documentosInlinks = []
                for link in list(set(auxiliarBackLinks)):
                    unDocumentoBack = next((x for x in unaListaDocumentos if x.url == link), None)
                    documentosInlinks.append(unDocumentoBack)
                unDocumento.inlinks = documentosInlinks


        self.calcular_Crank(unaListaDocumentos)

        for cloud in clouds:
            for n in cloud.graph.nodes():
                cloud.graph.node[n]['weight_CRANK'] = next((x for x in unaListaDocumentos if x.url == n), None).score

                        #print self.levels
    def contains(self,list, filter):
        for x in list:
            if filter(x):
                return True
        return False

    def backLinks(self,cloud,node,repeat):
        if repeat<self.back:
            repeat+=1
            if len(cloud.graph.predecessors(node))!=0:
                self.levels.append(cloud.graph.predecessors(node))
                for n in cloud.graph.predecessors(node):
                    self.backLinks(cloud,node,repeat)

    def coord(self,documento, consulta):
        contador = 0
        for word in consulta:
            if word in documento.pattern.words:
                contador +=1
        return (contador / len(consulta))

    def norm(self,documento, un_termino):
        valor = 0
        if un_termino in documento.pattern.vector:
            valor = documento.pattern.vector[un_termino]
        return valor

    def calcular_score_relevance_crank(self,doc,consulta,model):
        score_relevance = 0
        var_coord = self.coord(doc,consulta)
        for termino in consulta:
            # score_relevance += doc.pattern.tfidf(termino) * self.norm(doc,termino)*var_coord
            score_relevance += self.norm(doc,termino)*var_coord * model.document(doc.url).vector.get(termino,0)
        doc.score_relevance = score_relevance

    def calcular_score_inlinks(doc):
       score = 0
       for inlink in doc.inlinks:
           if inlink != doc:
               if len(inlink.inlinks) > 0:
                   for aux_inlink in inlink.inlinks:
                       if aux_inlink != doc:
                           score += aux_inlink.score_relevance
                   return score
               else:
                   return 0

       return score

    def calcular_score_contribution(self,doc,nivel,analizados):
        score = 0;

        if nivel < 4:
            if not doc in analizados:
                analizados.append(doc)
                if doc.inlinks:
                    for inlink in doc.inlinks:
                        score += self.calcular_score_contribution(inlink,nivel+1,analizados)
                        if inlink.inlinks:
                            score_inlink = 0
                            for aux_inlink in inlink.inlinks:
                                score_inlink += aux_inlink.score_relevance
                            if inlink.score_relevance+score_inlink > 0:
                                score += (doc.score_relevance/(inlink.score_relevance+score_inlink))*inlink.score_relevance
                            else:
                                score += doc.score_relevance
                        else:
                            score += doc.score_relevance
        return score
    def calcular_Crank(self,unaListaDocumentos):
        print "SCORE RELEVANCE"
        for doc in unaListaDocumentos:
            analizados = []
            doc.score_contribution = self.calcular_score_contribution(doc,0,analizados)
            doc.score = 0.80 * doc.score_relevance + 0.20 * doc.score_contribution
            print doc.score_relevance
##end##

class DocumentoCrank:
    url = ""
    contenido = ""
    pattern = ""
    score_crank = 0
    score_contribution = 0
    score_relevance = 0
    score_inlink = 0
    inlinks = []
