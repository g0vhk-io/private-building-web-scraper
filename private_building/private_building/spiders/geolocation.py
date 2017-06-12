import scrapy
import json
import urllib
from lxml import etree
class BuildingSearchSpider(scrapy.Spider):
    name = "address_geo"

    def start_requests(self):
        with open(self.input_file, "r") as f:
            buildings = json.loads(f.read())
            print(len(buildings))
            for b in buildings:
                address = b["address_1"]
                print(address)
                yield self.request_als(address)

    def request_als(self, a):
        url = "https://www.als.ogcio.gov.hk/lookup?" + urllib.parse.urlencode({"q":a})
        return scrapy.Request(url=url,callback=self.get_lat_lng, meta={'address': a})

    def get_lat_lng(self, response):
        elements = response.xpath("//PremisesAddress")
        address = response.meta['address']
        result = {"address": address, "lat": 0.0 , "lng": 0.0}
        if len(elements) > 0:
            element = elements[0]
            geo = element.xpath("GeospatialInformation")[0]
            lat = ''.join(geo.xpath("Latitude/text()").extract()).strip()
            lng = ''.join(geo.xpath("Longitude/text()").extract()).strip()
            result = {"address":address, "lat": float(lat), "lng": float(lng)}
        yield result

