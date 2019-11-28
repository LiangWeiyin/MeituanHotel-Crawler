# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class MeituanPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db, mongo_user, mongo_password):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                mongo_host= crawler.settings.get('MONGO_HOST'),
                mongo_port= crawler.settings.get('MONGO_PORT'),
                mongo_db= crawler.settings.get('MONGO_DATABASE'),
                mongo_user= crawler.settings.get('MONGO_USER'),
                mongo_password= crawler.settings.get('MONGO_PASSWORD')
                )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_host, int(self.mongo_port))
        self.db = self.client[self.mongo_db]
        self.db.authenticate(self.mongo_user, self.mongo_password, mechanism='SCRAM-SHA-1')

    def close_spoder(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['hotel'].insert_one(dict(item))
        return item
