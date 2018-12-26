#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanDiarySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    create_datetime = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
