from pattern.vector import Document, Model

d1 = Document('The cat purrs.', name='cat1')
d2 = Document('Curiosity killed the cat.', name='cat2')
d3 = Document('The dog wags his tail.', name='dog1')
d4 = Document('The dog is happy.', name='dog2')

m = Model([d1, d2, d3, d4])
m.reduce(4)
 
for d in m.documents:
    print
    print d.name
    for concept, w1 in m.lsa.vectors[d.id].items():
        print m.lsa.vectors[d.id].items() #matriz U
        for feature, w2 in m.lsa.concepts[concept].items():
            #print m.lsa.concepts[concept].items() #matriz Vt
            if w1!=0 and w2!=0:
                print (feature, w1 * w2)