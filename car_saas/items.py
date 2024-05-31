import scrapy

class CarItem(scrapy.Item):
    year = scrapy.Field()
    manufacturer = scrapy.Field()
    model = scrapy.Field()
    engine_size = scrapy.Field()
    car_type = scrapy.Field()
    price = scrapy.Field()
