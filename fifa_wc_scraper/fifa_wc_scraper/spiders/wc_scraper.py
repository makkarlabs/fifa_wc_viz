from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.http import Request
from scrapy.selector import Selector

url = ''

class wc_scraper(Spider):
  name = 'WC_Scraper'
  allowed_domains = ['en.wikipedia.org']
  start_urls = ['http://en.wikipedia.org/wiki/FIFA_World_Cup']
  
  def enc(st):
    return st.encode('ascii','ignore')

  def parse(self, response):
    extractor = SgmlLinkExtractor(allow =('wiki/[0-9]{4}\_FIFA\_World\_Cup$'))
    links = extractor.extract_links(response)
    for i in links:
      if int(i.text[:4]) < 2014:
        yield Request(i.url, callback=self.parse_items)  
    print 'over machi'

  def parse_items(self, response):
    sel = Selector(response)
    matches = sel.xpath('//*[@id="mw-content-text"]/div[contains(@class, "vevent")]').extract()
    for m in matches:
      m_date = enc(m[0].xpath('./table[1]/tr/td/div/text()').extract()[0])
      m_time = enc(m[0].xpath('./table[1]/tr/td/div/a/text()').extract()[0])


