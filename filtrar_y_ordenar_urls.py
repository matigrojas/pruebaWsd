from pattern.web import URL
import re

def filtrar_y_ordenar_urls(urls):
    
    #crea la lista distinctUrls, y agrega en esa lista las url, sacando las repetidas
    distinctUrls = []
    for i in urls:
        for m in i:
            if m not in distinctUrls:
                if not detect(m):
                    distinctUrls.append(m)
   
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

    weightedUrls = sorted(weightedUrls,key = lambda k: k[1],reverse=True)
    return weightedUrls

#filtra las Urls de facebook, amazon.. etc..
def detect(link):
    badLinks='youtube|linkedin|amazon|books.google|facebook|twitter|instagram|plus.google|yahoo|ebay|ebayinc|flickr|t.co|.google.|youtu.be|microsoft|microsoftstore'
    url=URL(link)
    #print url.domain
    if re.search(badLinks,url.domain)!=None:
        bad=True
    else:
        bad=False
    return bad