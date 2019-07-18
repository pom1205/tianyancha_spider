# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

USERNAME = 'root'
# PASSWORD = '271255542'
PASSWORD = 'newhope'
PORT = 3306
# HOST = '127.0.0.1'
HOST = '192.168.1.31'
DB = 'tycinformation'
# DB = 'tianyanchainfor'

class SsbasePipeline(object):

    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.password = PASSWORD
        self.user = USERNAME
        self.db = DB
        self.conn = pymysql.connect(host= self.host, user= self.user, port= self.port, password= self.password, db=self.db,charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        cursor = self.cursor
        sql = '''
                UPDATE `prdlicencecodeforbase` SET `name`= "%s",`toTime`= "%s",`estiblishTime`= "%s",`companyOrgType`= "%s",`regCapital`= "%s",
                `legalPersonName`= "%s",`regLocation`= "%s",`regInstitute`= "%s",`regStatus`= "%s",`email`= "%s",`percentileScore`= "%s",
                `businessScope`= "%s",`approvedTime`= "%s",`regNumber`= "%s",`phoneNumber`= "%s",`gettime`= "%s" where `creditCode`= "%s"
               '''
        cursor.execute(
            sql % (item['name'], item['toTime'], item['estiblishTime'], item['companyOrgType'],
                   item['regCapital'], item['legalPersonName'], item['regLocation'], item['regInstitute'],
                   item['regStatus'], item['email'], item['score'],
                   item['businessScope'], item['approvedTime'], item['regNumber'], item['phoneNumber'], item['gettime'],item['creditCode']
                   ))
        self.conn.commit()
        return item
