import scrapy

class MeteliSpider(scrapy.Spider):
    name = 'meteli'
    start_urls = ['http://www.meteli.net/jyvaskyla']
    
    def parse(self, response):
        SET_SELECTOR = 'div.event-list'
        for event in response.css(SET_SELECTOR):
            
            yield {
                'name': event.css('h2 ::text').extract_first(),
                'date': event.css('a:nth-child(1) > span:nth-child(1) > span:nth-child(1) ::text').extract_first() + '2019',
                'location': event.css('a:nth-child(1) > span:nth-child(4) > h4:nth-child(2) > span:nth-child(1) > span:nth-child(2) ::text').extract_first()[:-11],
                'image': event.css('.event-thumbnail img::attr(src)').extract_first(),
                'url': 'http://www.meteli.net' + event.css('a::attr(href)').extract_first()
            }

        NEXT_PAGE_SELECTOR = '.page-next::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
        