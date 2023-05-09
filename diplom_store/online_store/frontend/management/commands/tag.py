import scrapy
import json


class CitylinkSpider(scrapy.Spider):
    name = "citylink"
    start_urls = ["https://www.citylink.ru/catalog/kompyutery_i_komplektuyushchie/"]

    def parse(self, response):
        for product in response.css(".product"):
            name = product.css(".product-name a::text").get().strip()
            price = product.css(".product-price span::text").get().strip()
            description = product.css(".product-description::text").get().strip()
            characteristics = {}
            for row in product.css(".product-props tr"):
                key = row.css("td:first-child::text").get().strip()
                value = row.css("td:last-child::text").get().strip()
                characteristics[key] = value
            images = product.css(".product-photo img::attr(src)").getall()
            rating = product.css(".product-rating__value::text").get()
            categories = response.css(".breadcrumbs a::text").getall()
            tags = product.css(".product-tags a::text").getall()

            yield {
                "name": name,
                "price": price,
                "description": description,
                "characteristics": characteristics,
                "images": images,
                "rating": rating,
                "categories": categories,
                "tags": tags,
            }

        next_page = response.css(".next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
#scrapy crawl citylink -o output.json
