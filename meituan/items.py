# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class hotelItem(scrapy.Item):
    name = scrapy.Field()
    saleCount = scrapy.Field()
    addr = scrapy.Field()
    city = scrapy.Field()
    lowestPrice = scrapy.Field()
    hotelStar = scrapy.Field()
    scoreInfo = scrapy.Field()
    poiid = scrapy.Field()
    url = scrapy.Field()
    pic = scrapy.Field()
    phone = scrapy.Field()
    areaName = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    intro = scrapy.Field()





