
def filtrar_y_ordenar_urls(urls):
    
    #crea la lista distinctUrls, y agrega en esa lista las url, sacando las repetidas
    distinctUrls = []
    for i in urls:
        for m in i:
            if m not in distinctUrls:
                distinctUrls.append(m)
    print distinctUrls
   
    m = urls.__len__()
    weightedUrls = []

    for n in distinctUrls:
        valueEstimation = 0.0

        for url in urls:
            if url.count(n):
                position = url.index(n) + 1
                #print "la posicion de" , n , "es", position
                if position > 0:
                    valueEstimation += 1.0 / position
                    
        valueEstimation = valueEstimation / m
        weightedUrls.append((n , valueEstimation))

    weightedUrls.sort()
    return weightedUrls

#aca comienza el programa y ingreso las urls
urls = []
#creo un vector en cual tiene dos link por posicion
for n in range(0, 3):
    aa = []
    for m in range(0 , 2):
        link = raw_input("ingrese el link ") 
        if link != None: 
            aa.append(link)
    urls.append(aa)     
print urls

#llamo a la funcion y le paso las urls
aux = filtrar_y_ordenar_urls(urls)
print aux


