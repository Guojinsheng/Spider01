# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    table_name = 'book'
    # define the fields for your item here like:
    book_id = scrapy.Field()
    book_title = scrapy.Field()
    book_name = scrapy.Field()
    book_url = scrapy.Field()
    pass
class SectionItem(scrapy.Item):
    table_name = 'section'
    book_id = scrapy.Field()
    section_id = scrapy.Field()
    section_title = scrapy.Field()
    section_url = scrapy.Field()