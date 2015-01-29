import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from twisted.internet import reactor
from twisted.internet import task
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient as MC
import time
import datetime

# Exceptionally bad code!!!!

class PastebinItem(scrapy.Item):
    # define the fields that need to be retrieved for crawling

    url = scrapy.Field()
    paste = scrapy.Field()
    time = scrapy.Field()
    uniq_visitors = scrapy.Field()


class PastebinSpider(CrawlSpider):

    name = 'pastebin'
    allowed_domains = ['pastebin.com']
    start_urls = ['http://www.pastebin.com/archive']
    rules = [Rule(LinkExtractor(allow=['/[a-zA-Z]*\d*']), 'parse_items')]
    client = MC()
    db = client.DeloitteDemo
    collection = db.pastebin
    #collection.remove({'p':[]})
    def parse_items(self, response):
        try:

            items = PastebinItem()
            items['url'] = response.url
            items['paste'] = response.xpath("//textarea[@id='paste_code']/text()").extract()
            items['time'] = response.xpath("//div[@class='paste_box_line2']//span[1]/@title").extract()
            items['uniq_visitors'] = response.xpath("//div[@class='paste_box_line2']//span[2]/text()").extract()
            entry = {'u': items['url'], 'p': items['paste'], 't': items['time'], 'uv': items['uniq_visitors']}
            self.collection.insert(entry)
        except:
            print "Something went wrong"


def run():
    print "pastebin!!!"
    spider = PastebinSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    #crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    print "Pastebin scraping has finished"
    print "Iteration: " + str(datetime.datetime.now())


def iterate(interval):
    l = task.LoopingCall(run)
    l.start(interval) # call every second

    # l.stop() will stop the looping calls
    reactor.run(installSignalHandlers=0)
    #     run()
    #     print "Iteration: " + str(datetime.datetime.now())
    #     time.sleep(interval)
