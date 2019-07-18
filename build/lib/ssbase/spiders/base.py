# -*- coding: utf-8 -*-
import scrapy
import random
from selenium import webdriver
import redis
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree
import sys
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from scrapy import Spider,Request
from ssbase.items import SsbaseItem
from ssbase.usecookie import getcookie1, getcookie2, getcookie3, getcookie4


class BaseSpider(scrapy.Spider):
    name = 'base'
    allowed_domains = ['tianyancha.com']
    redis = redis.StrictRedis(host='192.168.1.32', port=6379, decode_responses=True)

    def start_requests(self):
        code = self.redis.lpop('base')
        # code = '915203003142744348'
        url = 'https://www.tianyancha.com/search?key={}'.format(code)
        yield scrapy.Request(url, callback=self.parse, meta={'code': code}, )

    def parse(self, response):
        redis = self.redis
        re_url = re.compile(r'https://www.tianyancha.com/company/\d+')
        code = response.meta['code']
        url = re_url.findall(response.text)
        if len(url) > 0:
            url = url[0]
            redis.lpush('lawcourt',code)
            province = response.xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/span/text()').extract_first()
            score = response.xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[4]/span[1]/text()').extract_first()
            yield scrapy.Request(url, callback=self.parse_second, meta={'url_link': url, 'code': code, 'province':province, 'score':score})
        else:
            redis.rpush('base', code)
            code = redis.lpop('base')
            print(self.redis.llen('base'))
            url = 'https://www.tianyancha.com/search?key={}'.format(code)
            yield scrapy.Request(url, callback=self.parse, meta={'code': code}, dont_filter=True)

    def parse_second(self, response):
        infor = SsbaseItem()
        code = response.meta['code']
        url = response.meta['url_link']
        score = response.meta['score']
        province = response.meta['province']
        infor['toTime'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[7]/td[2]/span/text()').extract_first()
        # infor['toTime'] = '2014-10-1'
        infor['estiblishTime'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/div/text()').extract_first()
        infor['companyOrgType'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[5]/td[2]/text()').extract_first()
        infor['regCapital'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/div/text()').extract_first()
        infor['legalPersonName'] = response.xpath(
            '//*[@id = "_container_baseInfo"]/table[1]/tbody/tr[1]/td[1]/div/div[1]/div[2]/div[1]/a/text()').extract_first()
        infor['regLocation'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[10]/td[2]/text()').extract_first()
        infor['regInstitute'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[6]/td[4]/text()').extract_first()
        infor['regStatus'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[2]/td[4]/text()').extract_first()
        infor['email'] = response.xpath('//*[@class = "email"]/text()').extract_first()
        infor['creditCode'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]/text()').extract_first()
        infor['businessScope'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[11]/td[2]//text()').extract_first()
        infor['approvedTime'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[6]/td[2]/text()').extract_first()
        infor['regNumber'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]/text()').extract_first()
        infor['score'] = score
        infor['phoneNumber'] = response.xpath('//div[@class = "detail"]/div[1]/span[2]/text()').extract_first()
        infor['gettime'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        infor['name'] = response.xpath('//h1[@class ="name"]//text()').extract_first()
        yield infor
        redis = self.redis
        code = redis.lpop('base')
        print(self.redis.llen('base'))
        url = 'https://www.tianyancha.com/search?key={}'.format(code)
        yield scrapy.Request(url, callback=self.parse, meta={'code': code}, dont_filter=True)

