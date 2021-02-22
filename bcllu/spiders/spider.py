import scrapy

from scrapy.loader import ItemLoader
from ..items import BclluItem
from itemloaders.processors import TakeFirst


class BclluSpider(scrapy.Spider):
	name = 'bcllu'
	start_urls = ['https://www.bcl.lu/fr/media_actualites/communiques/index.html']

	def parse(self, response):
		post_links = response.xpath('//li[@class="newsListItem"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="column2-content"]//p/text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="comm_date"]/text()').get()

		item = ItemLoader(item=BclluItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
