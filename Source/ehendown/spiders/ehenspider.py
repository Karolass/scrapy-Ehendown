# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.crawler import Settings

from scrapy.crawler import Crawler
from ehendown.items import EhendownItem

import re
from os import path

class ehenSpider(Spider):
    name = "ehendown"
    allowed_domains = ["g.e-hentai.org"]
    start_urls = (
        #'http://www.g.e-hentai.org/',
        #'http://g.e-hentai.org/g/831429/65af285e07/',
    )

    page_count, next_page_count = 1, 1

    def __init__(self, *args, **kwargs): 
        super(ehenSpider, self).__init__(*args, **kwargs) 
        #super(ehenSpider, self).set_crawler(crawler)

        self.start_urls = [kwargs.get('start_url')] 
    #    if kwargs.get('store_path') != '':
    #        se = Settings()
    #        se.set('IMAGES_STORE', kwargs.get('store_path'))
            #se.set('LOG_FILE', path.join(kwargs.get('store_path'), 'log.log'))

    def parse(self, response):
        
        sel = Selector(response)
        title = sel.xpath('//div/div[@id="gd2"]/h1[@id="gj"]/text()').extract()[0]
        p = re.compile('[!|?|\\|/]') 
        title = re.sub(p, '', title)        
        sites = sel.xpath('//div[@id="gdt"]/div[@class="gdtm"]')

        next_page = ''
        if sel.xpath('(//table/tr/td[@onclick="sp({0})"])/a/@href'.format(self.next_page_count)).extract() != []:
            next_page = sel.xpath('(//table/tr/td[@onclick="sp({0})"])/a/@href'.format(self.next_page_count)).extract()[0]
            self.next_page_count += 1
        
        for site in sites:
            item = EhendownItem()
            item['title'] = title
            item['page'] = '{0:0>3d}'.format(self.page_count)
            item['image_page'] = site.xpath('div/a/@href').extract()[0]
            request = Request(item['image_page'], callback = self.parse_image)
            request.meta['item'] = item
            self.page_count += 1
            yield request

        print('page: ' + next_page)
        print(self.page_count)
        if next_page:
            yield Request(next_page, callback=self.parse)

    def parse_image(self, response):

        item = response.meta['item']
        sel = Selector(response)
        item['image_link'] = sel.xpath('//div/a/img[@id="img"]/@src').extract()[0]

        return item

