#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from douban_diary_spider.settings import TARGET_NODE_URL
from douban_diary_spider.items import DoubanDiarySpiderItem


class DiarySpiderSpider(scrapy.Spider):
    name = 'douban_daily'
    allowed_domains = ['douban.com']
    start_urls = []
    note_url = TARGET_NODE_URL

    def parse(self, response):
        """
        处理单独一篇日记
        :param response:
        :return:
        """
        item = DoubanDiarySpiderItem()

        item['url'] = response.url
        item['title'] = response.xpath('//*[@class="note-container"]/div[1]/h1/text()').extract()[0]
        item['create_datetime'] = response.xpath('//*[@class="note-container"]/div[1]/div/*[@class="pub-date"]/text()').extract()[0]
        item['content'] = response.xpath('//*[@id="link-report"]').extract()[0]
        item['image_urls'] = response.xpath('//*[@id="link-report"]/*[@class="cc"]/table/tr/td/img/@src').extract()

        yield item

    def start_requests(self):
        """
        第一个请求的入口(进入某个用户的日记页面)
        :return:
        """
        yield scrapy.Request(self.note_url, callback=self.parse_all_diary_page)

    def parse_all_diary_page(self, response):
        """
        进入到列出所有日记的页面，获取各日记的url和下一页的url
        :param response:
        :return:
        """
        diary_urls = response.xpath('//*[@class="note-container"]/@data-url').extract()
        print(diary_urls)
        for url in diary_urls:
            yield scrapy.Request(url, dont_filter=True)

        next_page = response.xpath('//*[@id="content"]/div/div[1]/div[34]/span[3]/link/@href').extract()
        if len(next_page) > 0:
            # 有下一页
            yield scrapy.Request(next_page[0], callback=self.parse_all_diary_page)

