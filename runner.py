from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from goodsparcer import settings
from goodsparcer.spiders.lmerlin import LmerlinSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule(settings)

    process = CrawlerProcess(crawler_setting)
    query_str = input("Введите название категории товаров: ")
    process.crawl(LmerlinSpider, query_str=query_str)

    process.start()