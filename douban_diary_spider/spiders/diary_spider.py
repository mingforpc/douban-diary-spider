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
    login_url = 'https://www.douban.com/accounts/login'
    account = ''
    password = ''

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
        item['image_urls'] =response.xpath('//*[@id="link-report"]/div[class="cc"]/table/tbody/tr/td/img/@src').extract()

        print(item)
        yield item

    def start_requests(self):
        """
        第一个请求的入口(进入登录页面)
        :return:
        """
        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        """
        进入了登陆页面
        :param response:
        :return:
        """
        captcha_img_url = response.xpath('//*[@id="captcha_image"]/@src').extract()
        self.login_response = response
        if len(captcha_img_url) == 0:
            # 无需验证码
            form_data = {"source": "None", "redir": "https://www.douban.com", "form_email": self.account,
                         "form_password": self.password, "remember": "on", "login": "登录"}

            yield scrapy.FormRequest.from_response(response, formdata=form_data, callback=self.parse_login)
        else:
            # 需要验证码，把验证码下载下来
            captcha_img_url = captcha_img_url[0]
            yield scrapy.Request(captcha_img_url, callback=self.download_captcha_img)

    def download_captcha_img(self, response):
        """
        下载了验证码，手动输入....(懒得去注册接口进行orc识别)
        :param response:
        :return:
        """
        try:
            captcha_img = open(CURRENT_PATH + '/' + 'captcha.jpg', 'wb+')
            captcha_img.write(response.body)

            captcha = input("请打开目录[%s]下的captcha.jpg, 并输入验证码:" % CURRENT_PATH)

            form_data = {"source": "None", "redir": "https://www.douban.com", "form_email": self.account,
                         "form_password": self.password, "remember": "on", "login": "登录", "captcha-solution": captcha}
            yield scrapy.FormRequest.from_response(self.login_response, formdata=form_data, callback=self.parse_login)
        except Exception as ex:
            print("创建验证码图片文件失败,请检查: %s" % ex)
            exit(0)

    def parse_login(self, response):
        """
        提交了登录表单后的处理，判断是否登录成功
        :param response:
        :return:
        """
        mine_url = response.xpath('//*[@id="db-global-nav"]/div/div[1]/ul/li[2]/div/table/tbody/tr[1]/td/a/@href').extract()
        if len(mine_url) == 0:
            print("登录失败, 请重新执行脚本!")
            exit(0)
        else:
            mine_url = mine_url[0]
            yield scrapy.Request(mine_url, callback=self.parse_mine_page)

    def parse_mine_page(self, response):
        """
        进入到个人主页,需要获取日记页面的url
        :param response:
        :return:
        """
        all_diary_url = response.xpath('//*[@id="usr-profile-nav-notes"]/@href').extract()
        all_diary_url = all_diary_url[0]

        yield scrapy.Request(all_diary_url, callback=self.parse_all_diary_page)

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

