from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.http import Request
from scrapy.selector import Selector

import json

url = ''
def enc(st):
  return st.encode('ascii','ignore')

class wc_scraper(Spider):
  name = 'WC_Scraper'
  allowed_domains = ['en.wikipedia.org']
  start_urls = ['http://en.wikipedia.org/wiki/FIFA_World_Cup']

  def is_number(s):
    try:
      int(s)
      return True
    except ValueError:
      return False

  def parse(self, response):
    extractor = SgmlLinkExtractor(allow =('wiki/[0-9]{4}\_FIFA\_World\_Cup$'))
    links = extractor.extract_links(response)
    for i in links:
      if int(i.text[:4]) < 2014:
        print i.url
        #yield Request(i.url, callback=self.parse_items)  
    print 'over machi'

  def parse_items(self, response):
    sel = Selector(response)
    matches = sel.xpath('//*[@id="mw-content-text"]/div[contains(@class, "vevent")]')
    for m in matches:
      try:
        date = enc(m.xpath('./table[1]/tr/td/div/text()').extract()[0])
        time = enc(m.xpath('./table[1]/tr/td/div/a/text()').extract()[0])
        teams = m.xpath('./table[2]/tr/th/span/a/text()').extract()
        team_1_name = teams[0]
        team_2_name = teams[1]
        try: 
          score = m.xpath('./table[2]/tr/th/text()').extract()[0].split(u'\u2013')
        except:
          score = m.xpath('./table[2]/tr/th/a/text()').extract()[0].split(u'\u2013')
        team_1_goals = int(score[0].split('(')[0])
        team_2_goals = int(score[1].split('(')[0])
        f = open('output.csv', 'a')
        f.write(date + ',' + time + ',' + team_1_name + ',' + team_2_name + ',' + str(team_1_goals) + ',' + str(team_2_goals) + '\n')
        f.close()
        print date, time, teams, team_1_name, team_2_name, team_1_goals, team_2_goals
        #m_scorers = m[0].xpath('./table[2]/tr[2]/td')
        #m_team_1_scorers = m_scorers[0].xpath('.//text()').extract()
        #m_team_2_scorers = m_scorers[2].xpath('.//text()').extract()
      except:
        pass
