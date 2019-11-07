# -*- coding: utf-8 -*-
import scrapy

class UtopiaSpider(scrapy.Spider):
    name = 'utopia'
    allowed_domains = ['utopia.de']
    # scraping from list of best coffees
    start_urls = ['https://utopia.de/bestenlisten/bio-kaffee-fair-trade-kaffee/']
    def parse(self, response):
        list_of_urls = response.css("h3.product-listing__headline a::attr(href)").extract()
        for link in list_of_urls:
            request = scrapy.Request(link,callback=self.parse)
            yield request

        #extract brand name
        brand = response.css("h1::text").extract_first()
        #extract reviews
        reviews = response.css('div.commenttext p:nth-child(1)::text').extract()

        # self.log(reviews)
        
        for review in reviews:
            # counter for star-ratings based on number of i-class instances
            stars = 0
            for star in response.css("div.static-rating").extract():
                stars = star.count('<i class="fa fa-star" aria-hidden="true">')
            # dictionary for json
            coffee_reviews = {
            "brand":brand,
            "rating": stars,
            "review":review
            }
            yield coffee_reviews
        # follow pagination
        next_page_url =  response.css("ul.pagination > li > a::attr(href)").extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)