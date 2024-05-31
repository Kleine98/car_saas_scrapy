import re
import scrapy
from car_saas.items import CarItem

class ChobrodSpider(scrapy.Spider):
    name = "chobrod_spider"
    start_urls = ["https://chobrod.com/car-sale/p%d/" % i for i in range(1, 5)]

    custom_settings = {
        'FEEDS': {
            'data.json': {'format': 'json'},
        }
    }

    def parse(self, response):
        car_list = response.css('#wapper > div.page-car-listing > div > div:nth-child(2) > div.col-xs-8 > div.list-product > div')

        for car in car_list:
            name = car.css('div.info > div > h2 > a::text').get()
            price = car.css('div.info > div > p::text').get()

            pattern = r'(\d{4})\s+([^0-9]+)\s+(\w+)\s+([\d.]+)\s+([\w\s]+)'
            thai_pattern = r'[\u0E00-\u0E7F]+'  # Unicode range for Thai letters

            if name and price:
                match = re.match(pattern, name)
                if match:
                    year = match.group(1)
                    manufacturer = match.group(2).strip()
                    model = match.group(3)
                    engine_size = match.group(4)
                    car_type = re.sub(thai_pattern, '', match.group(5)).strip()

                    car_item = CarItem(
                        year=year,
                        manufacturer=manufacturer,
                        model=model,
                        engine_size=engine_size,
                        car_type=car_type,
                        price=price
                    )

                    yield car_item
