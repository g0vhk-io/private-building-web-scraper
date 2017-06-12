# private-building-web-scraper
## About
Scraper of https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true

## Dataset Available At
http://data.g0vhk.io/dataset/private-buildings-in-hong-kong-dataset

## Commands
### Setup
```bash
python3 -menv ./env
source ./env/bin/activate
pip install -r requirements.txt
```
### Running
#### Scraping Building Search Data
```bash
scrapy crawl building_search -t json -o output.json
```
#### Scraping Address Geocoding Data
```bash
scrapy crawl address_geo -t json -a input_file=output.json -o address.json
```
#### Combining Geocoding and Building Data
```bash
python combine.py -i output.json -a address.json -o result.csv
```
