import scrapy

class MenoinfoSpider(scrapy.Spider):
    name = 'menoinfo'
    start_urls = ['http://ksml.menoinfo.fi/events?f%5B0%5D=county%3AJyv%C3%A4skyl%C3%A4']
    
    def parse(self, response):
        SET_SELECTOR = '.view-menokatu-events-view .views-row'
        for event in response.css(SET_SELECTOR):
            
            yield {
                'name': event.css('div:nth-child(2) > h3:nth-child(1) > a:nth-child(1) ::text').extract_first(),
                'date': event.css('div:nth-child(3) > span:nth-child(1) ::text').extract_first(),
                'image': event.css('.views-row div.views-field-field-event-original-image img::attr(src)').extract_first(),
                'location': event.css('.event-place-wrapper ::text').extract_first()[12:],
                'url': 'http://ksml.menoinfo.fi' + event.css('h3 a::attr(href)').extract_first(),
                'category': event.css('a:nth-child(2) ::text').extract_first()
            }

        NEXT_PAGE_SELECTOR = '.pager-next a::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )