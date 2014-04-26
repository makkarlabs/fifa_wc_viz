from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.http import Request
from scrapy.selector import Selector

url = ''

class wc_scraper(Spider):
  name = 'WC_Scraper'
  allowed_domains = ['en.wikipedia.org']
  start_urls = ['http://en.wikipedia.org/wiki/FIFA_World_Cup']
  
  def parse(self, response):
    extractor = SgmlLinkExtractor(allow =('wiki/[0-9]{4}\_FIFA\_World\_Cup$'))
    links = extractor.extract_links(response)
    for i in links:
      print i
    print 'over'
