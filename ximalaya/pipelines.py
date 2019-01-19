# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class XimalayaPipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='0323',
            database='ximalaya',  # 数据库名
            charset='utf8'  # 编码：utf8mb4比utf8更大(占4个字节)的编码
        )
        self.cursor = self.db.cursor()
        self.i = 0

    # 每个yield的item都会进入这里
    def process_item(self, item, spider):
        print(item)
        keys, values = zip(*item.items())
        sql = "insert into `{}`({}) values({}) on duplicate key update {}".format(
            item.table_name,  # 表名
            ','.join(['`%s`' % key for key in keys]),  # 所有字段
            ','.join(['%s'] * len(values)),  # %s
            ','.join(['`{}`=%s'.format(key) for key in keys])
        )

        # 执行sql
        self.cursor.execute(sql, values * 2)
        self.db.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()
