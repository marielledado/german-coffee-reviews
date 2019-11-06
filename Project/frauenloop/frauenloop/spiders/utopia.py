# -*- coding: utf-8 -*-
import scrapy



class UtopiaSpider(scrapy.Spider):
    name = 'utopia'
    allowed_domains = ['utopia.de']
    url = ['https://utopia.de/produkt/j-j-darboven-cafe-intencion/']
    def parse(self, response):
        self.log("I just visited: " + response.url)
        reviews = response.css('div.commenttext p:nth-child(1)::text').extract()
        yield
        {
        "review":reviews
        }