import scrapy
import json

class AmazonProductSpider(scrapy.Spider):
    name = 'amazon_scraper'
    allowed_domains = ['amazon.in']

    def __init__(self, product_url=None, *args, **kwargs):
        super(AmazonProductSpider, self).__init__(*args, **kwargs)
        self.output_file = 'amazon_products.json'
        
        # Store the URL passed from run_spider.py
        if product_url:
            self.start_urls = [product_url]
        else:
            self.start_urls = []

    def parse(self, response):
        # Scrape the title
        title = response.css('#productTitle::text').get()
        if title:
            title = title.strip()

        availability = response.css('#availabilityInsideBuyBox_feature_div .a-size-medium::text').get().strip()
        if availability == 'In stock':
            availability = True
        else:
            availability=False
        # Scrape the price
        price = response.xpath('//div[@id="corePriceDisplay_desktop_feature_div"]//span[contains(@class, "a-price-whole")]/text()').get()
        # Scrape categories from the breadcrumb section
        categories = response.css('#wayfinding-breadcrumbs_feature_div .a-link-normal::text').getall()
        categories = [category.strip() for category in categories if category.strip()]

        # Prepare the scraped data
        scraped_data = {
            'request-status': 'OK',
            'product-title': title,
            'availability':availability,
            'price': price,
            'categories': categories,
        }

        # Write the scraped data to a CSV file
        self.write_to_json(scraped_data)

        # Return the scraped data
        return scraped_data

    def write_to_json(self, scraped_data):
        # Write or append data to a JSON file
        with open(self.output_file, 'a', encoding='utf-8') as jsonfile:
            json.dump(scraped_data, jsonfile, ensure_ascii=False, indent=4)
            jsonfile.write(',\n')  # To separate multiple entries
