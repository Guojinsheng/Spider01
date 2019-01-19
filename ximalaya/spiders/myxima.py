# -*- coding: utf-8 -*-
import re

import scrapy
from ..items import BookItem,SectionItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class MyximaSpider(CrawlSpider):
    name = 'myxima'
    allowed_domains = ['ximalaya.com']
    start_urls = ['https://www.ximalaya.com/youshengshu/wenxue/']
    # https://www.ximalaya.com/youshengshu/p2/
    rules = (
        Rule(
            LinkExtractor(
                allow=("/youshengshu/(.*?)/",),  # 允许的连接正则表达式
                restrict_xpaths=('//ul[@class="pagination-page tthf"]',),
            ),
            callback='parse_item',  # 回调函数
            follow=True,  # 是否跟随
        ),
    )


    # 获取到对应分类下的所有的url和对应的标题、id、书名
    def parse_item(self, response):
        print(response)
        book_list = response.xpath('//div[@class="content"]/ul/li')
        # print(book_list)
        for book in book_list:
            book_item = BookItem()
            id = book.xpath('./div/a/@href').get()
            id = ''.join(re.findall('/youshengshu/(.*?)/',id))
            book_item['book_id'] = id
            book_item['book_title'] = book.xpath('./div/a[@class="album-title line-2 lg  Iki"]/@title').get()
            book_item['book_name'] = book.xpath('./div/a[@class="album-author Iki"]/@title').get()
            book_item['book_url'] = 'https://www.ximalaya.com' + book.xpath('./div/a/@href').get()
            # print(book_item['book_url'])
            id = book.xpath('./div/a/@href').get()


            yield book_item
            request = scrapy.Request(book_item['book_url'],callback=self.parse_section)
            request.meta['book_id'] = book_item['book_id']
            request.meta['id'] = id
            request.meta['book_url'] = book_item['book_url']
            yield request

    # 将获取到的数据进行进一步的解析和爬取，直至爬取到想要的数据
    def parse_section(self,response):
        # print(response.text)
        secton_list = response.xpath('//div[@class="sound-list-wrapper rC5T"]//ul[@class="rC5T"]/li')




        for section in secton_list:
            section_item = SectionItem()
            section_item['book_id'] = response.meta['book_id']
            id = section.xpath('./div[@class="text rC5T"]/a/@href').get()
            list = id.split('/')
            # print(list)

            section_item['section_id'] = list[3]
            # print(section_item['section_id'])
            section_item['section_title'] = section.xpath('./div[@class="text rC5T"]/a/@title').get()
            section_item['section_url'] = 'https://www.ximalaya.com'+id
            yield section_item


        # page = 1
        # url = response.meta['book_url']
        # try:
        #     pages = int(response.xpath('//form[@class="tthf"]/input[@class="control-input tthf"]/@max'))
        #     for i in pages:
        #         url = url + '/p%d' %i
        #         print('*********************************************************************************************')
        #
        #     if page < pages:
        #         pass
        # except Exception as e:
        #     raise e