# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests

class XiaohuaSpiderPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'xiaohua':
            # print(item['folder_name'], item['img_name'], item['img_url'])
            base_dir = os.path.join(os.path.dirname(__file__), 'IMG')
            img_dir = os.path.join(base_dir, item['folder_name'])
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)
            img_path = os.path.join(img_dir, item['img_name'])

            img_url = item['img_url']
            resp = requests.get(img_url)
            if resp.status_code == 200:
                img_bytes = resp.content
            else:
                print('{}下载失败'.format(img_url))

            with open(img_path, mode='wb')as f:
                f.write(img_bytes)
            print('{}保存成功'.format(img_url))


            return item
