import scrapy
import json
import ass1_v2 as index
from bs4 import BeautifulSoup


seen = []
class QuotesSpider(scrapy.Spider):
    name = "essex"
    fileCount = 1
    

    def start_requests(self):
        start_urls = [
            'http://www.essex.ac.uk/'
        ]

        yield scrapy.Request(url=start_urls[0], callback=self.parse)

    def parse(self, response):
        if("html" in response.selector.root.getroottree().docinfo.doctype):
            dict1 = {}
            theIndex = {}
            innerIndex = {}

            innerIndex['_id'] = self.fileCount
            innerIndex['_index'] = 'essex'
            innerIndex['_type'] = 'webpage'
            
            theIndex['index'] = innerIndex

            dict1['title'] = response.css('title').extract()[0]
            dict1['url'] = response.url
            soup = BeautifulSoup(response.body, 'html.parser')
            dict1['bold'] = index.boldTags(soup)
            dict1['raw'] = index.stripHTML(soup,response.body.decode('utf-8'))
            
            
            self.fileCount += 1
            with open('essex.json', 'a') as f:
                f.write(json.dumps(theIndex))
                f.write('\n')
                f.write(json.dumps(dict1))
                f.write('\n')

            hrefs = response.css('a::attr(href)')
            for x in range(len(hrefs)):
                if(not (len(hrefs) == 0)):
                    if(hrefs[x].extract()[0] == '/'):
                        if(hrefs[x].extract() not in seen):
                            next_page = response.urljoin(hrefs[x].extract())
                            seen.append(hrefs[x].extract())
                            yield scrapy.Request(next_page, callback=self.parse)
                    
