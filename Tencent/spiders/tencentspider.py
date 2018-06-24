# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    baseURL = "https://hr.tencent.com/position.php?lid=&tid=&keywords=%E8%AF%B7%E8%BE%93%E5%85%A5%E5%85%B3%E9%94%AE%E8%AF%8D&start="
    offset = 0
    start_urls = [baseURL + str(offset)]

    def parse(self, response):

        node_list = response.xpath("//tr[@class ='even'] | // tr[@ class ='odd']")
        for node in node_list:
            item = TencentItem()

            # 提取每个职位的信息，并且将提取出的Unicode字符串编码为UTF-8
            item["position_name"] = node.xpath("./td[1]/a/text()").extract()[0]
            if len(node.xpath("./td[2]/text()")):
                item["position_type"] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item["position_type"] = ""
            item["people_number"] = node.xpath("./td[3]/text()").extract()[0]
            item["position_address"] = node.xpath("./td[4]/text()").extract()[0]
            item["release_time"] = node.xpath("./td[5]/text()").extract()[0]

            yield item

        # 方法一
        # if self.offset < 210:
        #     self.offset += 10
        #     url = self.baseURL + str(self.offset)
        #     # callback回调函数
        #     yield scrapy.Request(url, callback=self.parse)

        # 方法二：获取下一页的链接，调用callback函数
        if len(response.xpath("//a[@id='next' and @class='noactive']")) == 0:
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("https://hr.tencent.com/" + url, callback=self.parse)
