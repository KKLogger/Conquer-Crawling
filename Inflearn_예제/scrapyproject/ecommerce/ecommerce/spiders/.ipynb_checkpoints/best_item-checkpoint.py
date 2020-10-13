import scrapy
from ecommerce.items import EcommerceItem

class BestItemSpider(scrapy.Spider):
    name = 'best_item'
    allowed_domains = ['corners.gmarket.co.kr/Bestsellers']
    start_urls = ['http://corners.gmarket.co.kr/Bestsellers/']

    def parse(self, response):
        titles = response.css('div.best-list li > a::text').getall()
        for title in titles:
            doc = EcommerceItem()
            doc['title'] = title
            yield doc