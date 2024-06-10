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
            price_text = car.css('div.info > div > p::text').get()
            image_url = car.css('div.photo > a > img::attr(src)').get()
            details_page_url = car.css('div.photo > a::attr(href)').get()

            # Extract only numbers from the price text
            price = re.sub(r'[^\d]', '', price_text) if price_text else None

            pattern = r'(\d{4})\s+([^0-9]+)\s+(\w+)\s+([\d.]+)\s+([\w\s]+)'
            thai_pattern = r'[\u0E00-\u0E7F]+'  # Unicode range for Thai letters

            if name and price and image_url and details_page_url:
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
                        price=price,
                        image_url=image_url
                    )

                    # Follow the link to the car details page
                    request = scrapy.Request(
                        url=response.urljoin(details_page_url),
                        callback=self.parse_car_details
                    )
                    request.meta['car_item'] = car_item
                    yield request

    def parse_car_details(self, response):
        car_item = response.meta['car_item']

        # Use CSS selector to select the swiper slides and extract their style attribute
        slides_style = response.css('.swiper-slide::attr(style)').getall()

        # Use regex pattern to extract the image URLs from the style attribute
        car_item['swiper_images'] = [re.search(r'url\(["\']?(.*?)["\']?\)', style).group(1) for style in slides_style if re.search(r'url\(["\']?(.*?)["\']?\)', style)]

        yield car_item
