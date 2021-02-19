import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bancasempione.items import Article


class BancaSpider(scrapy.Spider):
    name = 'banca'
    start_urls = ['https://www.bancasempione.ch/News-dd578400']

    def parse(self, response):

        articles = response.xpath('//tr[@valign="top"]//div[@class="list_news_txt"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article.xpath('.//h2//text()').get()
            date = article.xpath('.//table//tr[1]/td[last()]//text()').get()
            if date:
                date = datetime.strptime(date.strip(), '%d.%m.%Y')
                date = date.strftime('%Y/%m/%d')

            content = article.xpath('.//table//tr[4]//text()').getall()
            content = [text for text in content if text.strip()]
            content = "\n".join(content).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()
