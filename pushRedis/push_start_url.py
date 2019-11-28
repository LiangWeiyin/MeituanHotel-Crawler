from redis import StrictRedis
from pymongo import MongoClient
import json
import random

def get_url():
    with open('./gx_urls.json', 'r') as f:
        temp = json.load(f)
    
    urls = [x + '&offset={}' for x in temp]
    return urls

if __name__ == "__main__":
    host = '10.3.9.133'
    redis_port = 6379
    start_url = 'hotel:start_urls'
    r =StrictRedis(host=host, port=redis_port, db=0, password='foobared')
    r.flushall()
    
    urls = get_url()
    random.shuffle(urls)

    for url in urls:
        r.lpush(start_url, url)
    
