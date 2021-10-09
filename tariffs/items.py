# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TariffsItem(scrapy.Item):
    t_date = scrapy.Field()
    time_from = scrapy.Field()
    time_to = scrapy.Field()
