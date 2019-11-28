# -*- coding: utf-8 -*-
import scrapy
import json
import re
from meituan.items import hotelItem
from scrapy_redis.spiders import RedisSpider

class HotelSpider(RedisSpider):
    name = 'hotel'
    allowed_domains = ['i.meituan.com', 'hotel.meituan.com']
    
    redis_key = 'hotel:start_urls'
    
    def make_requests_from_url(self, url):
        offset = 0
        meta = {
                'url': url,
                'offset': offset,
            }
        # print(url)
        return scrapy.Request(url=url.format(offset), meta=meta, dont_filter=True)

    # def start_requests(self):
    #     offset = 0
    #     for url in self.start_urls:
    #         meta = {
    #             'url': url,
    #             'offset': offset,
    #         }
    #         yield scrapy.Request(url=url.format(offset), meta=meta, callback=self.parse, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        next_url = meta['url']
        next_offset = meta['offset'] + 20
        next_meta = {
            'url': next_url,
            'offset': next_offset,
        }
        data = json.loads(response.text)
        if data['data']['searchresult']:
            hotels = data['data']['searchresult']
            for hotel in hotels:
                item = hotelItem()
                item['name'] = hotel['name']
                item['addr'] = hotel['addr']
                item['city'] = hotel['cityName']
                item['saleCount'] = hotel['historySaleCount']
                item['lowestPrice'] = hotel['lowestPrice']
                item['hotelStar'] = hotel['hotelStar']
                item['scoreInfo'] = hotel['scoreIntro']
                item['poiid'] = hotel['poiid']
                item['areaName'] = hotel['areaName']
                item['lat'] = hotel['lat']
                item['lng'] = hotel['lng']
                item['url'] = 'https://hotel.meituan.com/{}/'.format(hotel['poiid'])
                item['pic'] = re.sub(r'w.h', '750.0.0', hotel['frontImg'])
                yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.get_phone)

            yield scrapy.Request(url=next_url.format(next_offset), meta=next_meta, callback=self.parse, dont_filter=True)

        else:
            pass

    def get_phone(self, response):
        item = response.meta['item']
        string = re.findall(r'window.__INITIAL_STATE__={.+};', response.text)[0][25:-1]
        data = json.loads(string)
        item['phone'] = data['poiData']['phone']
        item['intro'] = re.sub(r'[\s]+', '', data['poiData']['introduction'])

        yield item
