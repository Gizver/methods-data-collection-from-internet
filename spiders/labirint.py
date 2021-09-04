import scrapy
from scrapy.http import HtmlResponse
from bookparcer.items import BookparcerItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/']

    def parse(self, response:HtmlResponse):

        urls = response.xpath('//a[@class="product-title-link"]/@href').getall()
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for url in urls:
            yield response.follow(url, callback=self.book_parse)

    def book_parse(self, response:HtmlResponse):
        book_url = response.url
        book_title = response.xpath("//h2/text()").get()
        book_author = response.xpath("//a[@data-event-label='author']/text()").getall()
        book_old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        book_new_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        book_rating = response.xpath("//div[@id='rate']/text()").get()
        item = BookparcerItem(url=book_url, title=book_title, author=book_author, old_price=book_old_price, new_price=book_new_price, rating=book_rating)
        yield item