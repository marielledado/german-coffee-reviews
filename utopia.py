# -*- coding: utf-8 -*-
import scrapy



class UtopiaSpider(scrapy.Spider):
    name = 'utopia'
    allowed_domains = ['utopia.de']
    start_urls = ['https://utopia.de/produkt/j-j-darboven-cafe-intencion/']
    def parse(self, response):
        self.log("I just visited: " + response.url)
        reviews = response.css('div.commenttext p:nth-child(1)::text').extract()

        # self.log(reviews)

        for review in reviews:
            stars = 0
            for star in response.css("div.static-rating").extract():
                stars = star.count('<i class="fa fa-star" aria-hidden="true">')
            coffee_reviews = {
            "brand":response.css("h1::text").extract(),
            "rating": stars,
            "review":review
            }
            yield coffee_reviews
        # follow pagination
        next_page_url =  response.css("ul.pagination > li > a::attr(href)").extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)