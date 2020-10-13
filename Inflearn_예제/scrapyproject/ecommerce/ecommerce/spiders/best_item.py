from time import process_time
import scrapy
from ecommerce.items import EcommerceItem


class BestItemSpider(scrapy.Spider):
    name = 'best_item'
    allowed_domains = ['corners.gmarket.co.kr/Bestsellers']
    start_urls = ['http://corners.gmarket.co.kr/Bestsellers/']

    def parse(self, response):
        titles = response.xpath(
            '//*[@id="gBestWrap"]/div/div/div/ul/li/a/text()').getall()
        prices = response.xpath(
            '//*[@id="gBestWrap"]/div/div/div/ul/li/div/div/strong/span/span/text()').getall()
        for title, price in zip(titles, prices):
            doc = EcommerceItem()
            doc['title'] = title
            doc['price'] = int(price.strip().replace('원', '').replace(',', ''))
            yield doc
