FROM python:3
MAINTAINER LiangWeiyin
ADD . /code
WORKDIR /code
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
CMD scrapy crawl hotel

