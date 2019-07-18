# -*- coding: utf-8 -*-
import scrapy
import redis
import time
import re
from ssbase.items import SsbaseItem



class BaseSpider(scrapy.Spider):
    #爬虫是按照需求搜索爬取指定的公司
    name = 'base'
    allowed_domains = ['tianyancha.com']
    redis = redis.StrictRedis(host='xxx.xxx.xx.xx', port=6379, decode_responses=True)
    # redis存储任务，所需爬取公司的名称

    def start_requests(self):
        code = self.redis.lpop('xxx')
        # key
        url = 'https://www.tianyancha.com/search?key={}'.format(code)
        yield scrapy.Request(url, callback=self.parse, meta={'code': code}, )

    def parse(self, response):
        redis = self.redis
        re_url = re.compile(r'https://www.tianyancha.com/company/\d+')
        # 获取公司详细页面链接
        code = response.meta['code']
        url = re_url.findall(response.text)
        if len(url) > 0:
            url = url[0]
            redis.lpush('xxx',code)
            province = response.xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/span/text()').extract_first()
            score = response.xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div[4]/span[1]/text()').extract_first()
            yield scrapy.Request(url, callback=self.parse_second, meta={'url_link': url, 'code': code, 'province':province, 'score':score})
        else:
            redis.rpush('xxx', code)
            code = redis.lpop('xxx')
            print(self.redis.llen('xxx'))
            url = 'https://www.tianyancha.com/search?key={}'.format(code)
            yield scrapy.Request(url, callback=self.parse, meta={'code': code}, dont_filter=True)

    def parse_second(self, response):
        infor = SsbaseItem()
        code = response.meta['code']
        url = response.meta['url_link']
        score = response.meta['score']
        province = response.meta['province']
        infor['toTime'] = response.xpath('//*[@id = "_container_baseInfo"]/table[2]/tbody/tr[7]/td[2]/span/text()').extract_first()
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


