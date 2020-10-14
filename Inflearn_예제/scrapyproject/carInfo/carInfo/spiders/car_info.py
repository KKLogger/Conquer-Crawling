import scrapy
from scrapy.utils.url import parse_url
from w3lib.url import parse_data_uri


class CarInfoSpider(scrapy.Spider):
    name = 'car_info'

    def start_requests(self):

        yield scrapy.Request(url='https://www.kbchachacha.com/public/search/main.kbc#!?_menu=buy', callback=self.parse_url)

    def parse_url(self, response):
        urls = reponse.css('a[class="checkListLink"]')
