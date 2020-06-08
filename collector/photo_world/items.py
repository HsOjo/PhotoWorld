# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    thumbs = scrapy.Field()
    date = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    type = scrapy.Field()
