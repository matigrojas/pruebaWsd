from pattern.web import Crawler

class Polly(Crawler): 
    def visit(self, link, source=None):
        print 'visited:', repr(link.url), 'from:', link.referrer
    def fail(self, link):
        print 'failed:', repr(link.url)

p = Polly(links=['http://www.clips.ua.ac.be/'], delay=3)

while not p.done:
    p.crawl(method=None, cached=False, throttle=3)