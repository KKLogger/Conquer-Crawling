import scrapy
from ecommerce.items import EcommerceItem


class CategoricalBestItemSpider(scrapy.Spider):
    name = 'categorical_best_item'
    # domain 제한 없앰
    # allowed_domains = ['corners.gmarket.co.kr/Bestsellers']
    # start_urls = ['http://corners.gmarket.co.kr/Bestsellers/']

    # start_urls에 자동화하여 url 삽입
    board_url = 'http://corners.gmarket.co.kr'
    start_url = 'http://corners.gmarket.co.kr/Bestsellers'

    def start_requests(self):
        # 메인 페이지에서 메인 카테고리의 즈소 크롤링
        yield scrapy.Request(url=self.start_url, callback=self.parse_main_category, dont_filter=True)

    def parse_main_category(self, response):
        urls = response.css(
            'div.gbest-cate ul.by-group li a::attr(href)').getall()
        titles = response.css('div.gbest-cate ul.by-group li a::text').getall()

        for title, url in zip(titles, urls):
            # 각 메인 카테고리의 아이템 크롤링
            yield scrapy.Request(url=self.board_url + url, callback=self.parse_item_info, meta={'main_category_name': title, 'sub_category_name': 'Main'}, dont_filter=True)
            # 긱 메인 카테고리의 서브카테고리 주소 크롤링
            yield scrapy.Request(url=self.board_url + url, callback=self.parse_sub_category, meta={'main_category_name': title}, dont_filter=True)

    def parse_sub_category(self, response):
        sub_category_urls = response.css(
            'div.navi.group ul > li > a::attr(href)').getall()
        titles = response.css(
            'div.navi.group ul > li > a::text').getall()
        for sub_category_url, title in zip(sub_category_urls, titles):
            # 각 서브 카테고리의 아이템 크롤링
            yield scrapy.Request(url=self.board_url + sub_category_url, callback=self.parse_item_info, meta={'main_category_name': response.meta['main_category_name'], 'sub_category_name': title}, dont_filter=True)

    def parse_item_info(self, response):

        item_infos = response.css('div.best-list')[1]
        item_infos = item_infos.css('ul li')

        for rank, item_info in enumerate(item_infos):
            item_rank = rank + 1
            item_name = item_info.css('a.itemname::text').get()
            item_o_price = item_info.css(
                'div.item_price div.o-price span span::text').get()
            item_s_price = item_info.css(
                'div.item_price div.s-price span span::text').get()
            sale_percent = item_info.css(
                'div.item_price div.s-price span em::text').get()

            # None 값 처리
            if item_o_price is None:
                item_o_price = item_s_price
            if sale_percent is None:
                sale_percent = "0%"
            item = EcommerceItem()
            item['main_category_name'] = response.meta['main_category_name']
            item['sub_category_name'] = response.meta['sub_category_name']
            item['name'] = item_name
            item['rank'] = item_rank
            item['o_price'] = item_o_price
            item['s_price'] = item_s_price
            item['sale_percent'] = sale_percent
            yield item
