# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SsbaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    toTime = scrapy.Field()
    estiblishTime = scrapy.Field()
    companyOrgType = scrapy.Field()
    regCapital = scrapy.Field()
    legalPersonName = scrapy.Field()
    regLocation = scrapy.Field()
    regInstitute = scrapy.Field()
    regStatus = scrapy.Field()
    email = scrapy.Field()
    creditCode = scrapy.Field()
    businessScope = scrapy.Field()
    approvedTime = scrapy.Field()
    regNumber = scrapy.Field()
    score = scrapy.Field()
    phoneNumber = scrapy.Field()
    lcode = scrapy.Field()
    gettime = scrapy.Field()
    name = scrapy.Field()

