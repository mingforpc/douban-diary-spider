#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy


class DiarySpiderSpider(scrapy.Spider):
    name = 'douban_daily'
    allowed_domains = ['douban.com']
    start_urls = []
    login_url = 'https://www.douban.com/accounts/login'
    account = ''
    password = ''

    def parse(self, response):
        print(response.txt)

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):

        captcha_img_url = response.xpath('//*[@id="captcha_image"]/@src').extract()

        if len(captcha_img_url) == 0:
            formdata = {"source": "None", "redir": "https://www.douban.com",
                        "form_email": self.account, "form_password": self.password,
                        "remember": "on", "login": "登录"}
            yield scrapy.FormRequest.from_response(response, formdata=formdata, callback=self.parse_login)
        else:
            captcha_img_url = captcha_img_url[0]
            yield scrapy.Request(captcha_img_url, callback=self.download_captcha_img)
            print(captcha_img_url)

    def download_captcha_img(self, response):
        print(response)


    def parse_login(self, response):
        print(response.txt)
        yield from super().start_requests()