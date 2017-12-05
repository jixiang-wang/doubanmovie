# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Doubanmovie250Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 电影名
    score = scrapy.Field()  # 豆瓣分数
    detail_url = scrapy.Field()  # 文章链接在首页爬取
    quote = scrapy.Field()  # 引用
    top = scrapy.Field()  # 排名
    year = scrapy.Field()  # 上映年份
    director = scrapy.Field()  # 导演
    scriptwriter = scrapy.Field()  # 编剧
    actor = scrapy.Field()  # 演员
    classification = scrapy.Field()  # 分类
    made_country = scrapy.Field()  # 制片国家/地区
    language = scrapy.Field()  # 语言
    showtime = scrapy.Field()  # 上映日期
    film_time = scrapy.Field()  # 片长
    alias = scrapy.Field()  # 别名
    IMDb_url = scrapy.Field()  # IMDb链接
    votes = scrapy.Field()  # 评价人数
    describe = scrapy.Field()  # 剧情简介

