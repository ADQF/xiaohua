# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from xiaohua_spider.items import XiaohuaSpiderItem

class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/hua/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept - Language': 'zh - CN, zh;q = 0.9',
            'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 71.0.3578.98Safari / 537.36'
        }
    }

    url_set = set()

    def parse(self, response):
        a_list = Selector(response).xpath('//div[@class="img"]/a')
        for a in a_list:
            detail_url = a.xpath('.//@href').extract_first()
            if detail_url in self.url_set:
                pass
            else:
                self.url_set.add(detail_url)
                gallery_url = detail_url.replace('/p', '/s')
                yield Request(url=gallery_url, callback=self.img_parse)

    def img_parse(self, response):
        src_list = Selector(response).xpath('//div[@class="inner"]/a/img/@src').extract()
        folder_name = Selector(response).xpath('//h1/text()').extract_first()

        for src in src_list:
            print('图片资源', src)
            img_url = src
            if img_url.startswith('https'):
                pass
            else:
                # 路由形式的，协议http，没有解析xiaohuar.com
                img_url = 'http://www.xiaohuar.com' + img_url

            img_name = src.split('/')[-1]   # 20190110AdOgzcLVqR.jpg

            # item = XiaohuaSpiderItem(folder_name=folder_name, img_name=img_name, img_url=img_url)
            item = XiaohuaSpiderItem()
            item['folder_name'] = folder_name
            item['img_name'] = img_name
            item['img_url'] = img_url
            yield item