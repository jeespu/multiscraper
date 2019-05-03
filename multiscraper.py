from scrapy.crawler import CrawlerProcess
# Import every spider
from spiders.menoinfo import MenoinfoSpider
from spiders.meteli import MeteliSpider
import os

process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': 'tempEvents.json'
        })
# Insert a crawl process for every spider here
process.crawl(MenoinfoSpider)
process.crawl(MeteliSpider)
process.start()

# Workaround for overwriting and not appending to the old "events.json",
# which Scrapy does by default
os.remove("events.json")
os.rename("tempEvents.json", "events.json")