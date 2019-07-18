# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from logging import getLogger
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
from io import BytesIO
from PIL import Image
import time
from selenium.webdriver import ActionChains
from ssbase.chaojiying import Chaojiying
import random
import redis
import json
import os

CHAOJIYING_USERNAME = ''
CHAOJIYING_PASSWORD = ''
CHAOJIYING_SOFT_ID = ''
CHAOJIYING_KIND = ''

usernames = []

class SsbaseSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SsbaseDownloaderMiddleware(object):

    def __init__(self):
        self.logger = getLogger(__name__)
        self.options = Options()
        self.options.add_argument('-headless')
        self.browser = webdriver.Firefox(firefox_options=self.options)
        self.wait = WebDriverWait(self.browser,10)
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __del__(self):
        self.browser.quit()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        #链接selenium
        rds = redis.StrictRedis(host='', port=6379, decode_responses=True)
        self.logger.debug('Selenium is Starting')
        try:
            users = random.choice(usernames)
            self.browser.get(request.url)
            self.browser.delete_all_cookies()
            for i in range(1, 16):
                c = rds.hget(users, 'cookies{}'.format(i))
                self.browser.add_cookie(json.loads(c))
            self.browser.get(request.url)
            # print(self.browser.page_source)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # return None

    def process_response(self, request, response, spider):
        #天眼查的点触验证码破解
        nowurl = self.browser.current_url
        if nowurl[8:17] == 'antirobot':
            self.run_verify()
            return response

        else:
            return response
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        self.browser.close()
        self.browser.quit()
        os.system('taskkill /im geckodriver.exe /F')
        os.system('taskkill /im firefox.exe /F')

    def get_touch_element(self):
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'new-box94')))
        return element

    def get_position(self):
        element = self.get_touch_element()
        time.sleep(2)
        location = element.location
        size = element.size
        print(location, size)
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        self.browser.get_screenshot_as_file('C:\\Users\Administrator\Desktop\prdabnormal.png')
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touch_image(self, name='captcha.png'):
        top, bottom, left, right = self.get_position()
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        # 截图位置必须为左上右下
        captcha.save(name)
        return captcha

    def get_points(self, captcha_result):
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations


    def click_words(self, locations):
        for location in locations:
            ActionChains(self.browser).move_to_element_with_offset(self.get_touch_element(), location[0],
                                                             location[1]).click().perform()
            time.sleep(1)

    def click_verify(self):
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'submitie')))
        button.click()

    def run_verify(self):
        chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
        image = self.get_touch_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        result = chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_KIND)
        locations = self.get_points(result)
        self.click_words(locations)
        self.click_verify()
