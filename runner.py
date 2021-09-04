from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from bookparcer import settings
from bookparcer.spiders.labirint import LabirintSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(crawler_settings)
    process.crawl(LabirintSpider)

    process.start()