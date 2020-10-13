# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class EcommercePipeline:
    def process_item(self, item, spider):
        if item['price'] > 10000:
            return item
        else:
            raise DropItem('drop item having lower price than 10000')
