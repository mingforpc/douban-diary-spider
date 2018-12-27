# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import html2text
import shutil
from douban_diary_spider.settings import DIARY_STORE, IMAGES_STORE, HEXO_TITLE_TEMPLATE


class DoubanDiarySpiderPipeline(object):

    def process_item(self, item, spider):

        url = item['url']
        title = item['title']
        create_datetime = item['create_datetime']
        content = item['content']
        image_urls = item['image_urls']
        images = item['images']

        # 文件或者文件夹的title名
        title_disk = title.replace("-", "_")

        # 创建hexo的图片文件夹
        os.mkdir(DIARY_STORE + '/' + title_disk)
        mdfile = open(DIARY_STORE + '/' + title_disk + ".md", "w+")

        hexo_title = HEXO_TITLE_TEMPLATE.format(title=title, date=create_datetime)

        mdfile.write(hexo_title)

        convert = html2text.HTML2Text()

        md_content = convert.handle(content)

        # 替换https的URL
        for image in images:
            image_url = image['url']
            current_path = IMAGES_STORE + '/' + image['path']
            target_path = DIARY_STORE + '/' + title_disk + '/' + os.path.basename(current_path)
            shutil.move(current_path, target_path)
            md_content = md_content.replace(str(image_url), "./" + os.path.basename(current_path))

        mdfile.write(md_content)

        return item
