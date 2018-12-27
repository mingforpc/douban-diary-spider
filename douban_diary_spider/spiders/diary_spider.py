#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import scrapy
from douban_diary_spider.items import DoubanDiarySpiderItem

CURRENT_PATH = os.getcwd()


class DiarySpiderSpider(scrapy.Spider):
    name = 'douban_daily'
    allowed_domains = ['douban.com']
    start_urls = []
    note_url = 'https://www.douban.com/people/xxxxx/notes'

    # TODO: 保存login页面的response
    login_response = None

    def parse(self, response):
        """
        处理单独一篇日记
        :param response:
        :return:
        """
        item = DoubanDiarySpiderItem()

        item['url'] = response.url
        item['time'] = response.xpath('//*[@class="note-container"]/div[1]/h1').extract()
        item['create_datetime'] = response.xpath('//*[@class="note-container"]/div[1]/div/*[@class="pub-date"]').extract()
        item['content'] = response.xpath('//*[@id="link-report"]').extract()
        item['image_urls'] = response.xpath('//*[@id="link-report"]/div[class="cc"]/table/tbody/tr/td/img/@src').extract()

        print(item)
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

