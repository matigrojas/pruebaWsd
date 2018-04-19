from pattern.web import URL
import re

class Filter:

    def __init__(self):
        self.badLinks='youtube|linkedin|amazon|books.google|facebook|twitter|instagram|plus.google|yahoo|ebay|ebayinc|flickr|t.co|.google.|youtu.be|microsoft|microsoftstore'

    def detect(self,link):
        url=URL(link)
        #print url.domain
        if re.search(self.badLinks,url.domain)!=None:
            bad=True
        else:
            bad=False
        return bad