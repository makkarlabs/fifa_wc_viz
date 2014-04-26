from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.http import Request
from scrapy.selector import Selector

import json

urls = ['http://www.fifa.com/tournaments/archive/worldcup/uruguay1930/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/italy1934/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/france1938/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/brazil1950/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/switzerland1954/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/sweden1958/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/chile1962/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/england1966/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/mexico1970/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/germany1974/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/argentina1978/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/spain1982/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/mexico1986/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/italy1990/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/usa1994/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/france1998/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/koreajapan2002/matches/index.html',
    'http://www.fifa.com/tournaments/archive/worldcup/germany2006/matches/index.html',
   'http://www.fifa.com/tournaments/archive/worldcup/southafrica2010/matches/index.html'
     ]
def enc(st):
  return st.encode('ascii','ignore')

class wc_scraper(Spider):
  name = 'WC_Archiver'
  allowed_domains = ['www.fifa.com']
  start_urls = urls
  #start_urls = ['http://en.wikipedia.org/wiki/FIFA_World_Cup']

  def __init__(self):
    f = open('master_wc.csv', 'w')
    f.write('date, venue, home, away, hscore, ascore, hpens, apens, winner\n')
    f.close()

  def find_winner(self, homeTeam, awayTeam, homeScore, awayScore):
    if int(homeScore) > int(awayScore):
      return homeTeam
    else:
      return awayTeam

  def parse(self, response):
    year = response.url.split('/')[-3][-4:]
    sel = Selector(response)
    fixtures = sel.xpath('//table[contains(@class, "fixture")]')
    for f in fixtures:
      matches = f.xpath('./tbody/tr')
      for m in matches:
        date = m.xpath('./td[contains(@class, "dt")]/text()').extract()[0]
        venue = m.xpath('./td[contains(@class, "v")]/text()').extract()[0]
        homeTeam = m.xpath('./td[contains(@class, "homeTeam")]/a/text()').extract()[0]
        awayTeam = m.xpath('./td[contains(@class, "awayTeam")]/a/text()').extract()[0]
        scoreStr = m.xpath('./td[contains(@class, "c")]')[2].xpath('.//a/text()').extract()[0]
        wouldBe = scoreStr.split(' ')
        (homeTeamTScore, awayTeamTScore) = wouldBe[0].split(':')
        homePenScore = 'NA'
        awayPenScore = 'NA'
        result = 'D'
        if homeTeamTScore == awayTeamTScore:
          try:
            if wouldBe[1] == 'a.e.t.':
              if wouldBe[-1] != 'PSO':
                raise IndexError
              (homePenScore, awayPenScore) = wouldBe[-2].split(':')
              result = self.find_winner(homeTeam, awayTeam, homePenScore, awayPenScore)
          except IndexError:
            pass
        else:
          result = self.find_winner(homeTeam, awayTeam, homeTeamTScore, awayTeamTScore)
        f = open('master_wc.csv', 'a')
        f.write(date + ' '+ year + ',' + enc(venue) + ',' + enc(homeTeam) + ',' + enc(awayTeam) + ',' + homeTeamTScore + ',' +  awayTeamTScore +','+ homePenScore +','+ awayPenScore + ','+ enc(result) + '\n')
        f.close()
        print date + ' '+ year, enc(venue), enc(homeTeam), enc(awayTeam), homeTeamTScore, awayTeamTScore, homePenScore, awayPenScore, enc(result)
