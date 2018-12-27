# douban-diary-spider

这是一个使用Scrapy的豆瓣日记爬虫，只会爬去指定用户的日记，并将其转为hexo可用的MarkDown格式。

## 使用

1. 在`douban_diary_spider/settings.py`中设置`TARGET_NODE_URL`的值，`TARGET_NODE_URL`是指定用户的日记主页，格式类似于:`https://www.douban.com/people/{xxxxxx}/notes`
2. 如果需要修改hexo的MarkDown头部模板，可以修改`douban_diary_spider/settings.py`中的`HEXO_TITLE_TEMPLATE`,目前只会设置日记名和时间。主要是hexo的文章都会有如下的头:

    ```
    ---
    title: 标题
    categories:
      - xxx
      - xxx
    date: 2018-12-14 14:04:42
    ---
    ```
3. 安装所需要的包, 在项目目录下执行`pip install -r requirements.txt`
4. 安装成功后执行`scrapy crawl douban_daily`
5. 如果爬取成功，日记将会以标题名存在`diary`文件夹中，同时会有同名的文件夹，用来保存日记中的图片（按照hexo的文章图片格式）