# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.http import Request
from scrapy.exceptions import DropItem
import json
import codecs
from ehendown.items import EhendownItem

class JsonWriterPipeline(object):

    #file1 = codecs.open('ehendown_comic.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):

        pfile = ""
        if isinstance(item, EhendownItem):
            pfile = self.file1

        line = json.dumps(dict(item), sort_keys=True,
                          indent=4, separators=(',', ': ')) + "\n"
        pfile.write(line.decode('unicode_escape'))
        return item

from scrapy.pipelines.images import ImagesPipeline
import re
from os import path 

class MyImagesPipeline(ImagesPipeline):
    
    CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')
    
    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict
    def get_media_requests(self, item, info):
        #print "get_media_requests"
        return [Request(item["image_link"], meta={
            'page': item["page"],
            'title': item["title"]
            })]

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        #print "get_images"

        for key, image, buf, in super(MyImagesPipeline, self).get_images(response, request, info):
            if self.CONVERTED_ORIGINAL.match(key):
                key = self.change_filename(key, response)
            #print key
            yield key, image, buf

    def change_filename(self, key, response):
        #print 'change_filename'
        return path.join('download', response.meta['title'], response.meta['page'] + ".jpg")

