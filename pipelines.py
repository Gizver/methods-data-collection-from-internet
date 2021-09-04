# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BookparcerPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books


    def process_item(self, item, spider):
        item['author'] = ', '.join(item['author'])
        item['old_price'] = int(item['old_price'])
        item['new_price'] = int(item['new_price'])
        item['rating'] = float(item['rating'])
        new_item = dict(item)
        collection = self.mongobase[spider.name]
        collection.insert_one(new_item)
        return item
