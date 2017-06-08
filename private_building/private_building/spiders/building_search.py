import scrapy
import re
from bs4 import BeautifulSoup

class BuildingSearchSpider(scrapy.Spider):
    name = "building_search"

    def start_requests(self):
        url = "https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true"
        yield scrapy.Request(url=url, callback=self.parse_first_page, meta={'cookiejar':1}, dont_filter=True)
    

    def parse_view_state_page(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        view_state = soup.find_all("input", {"name":"javax.faces.ViewState"})[0].get('value')
        page_size = response.meta['page_size']
        i = response.meta['page_index']
        yield scrapy.FormRequest(url='https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true', 
                callback=self.parse_page,
                headers={'Accept-Encoding': 'gzip, deflate, br',
                         'X-Requested-With': 'XMLHttpRequest',
                         'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
                         'Faces-Request': 'partial/ajax',
                         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                         'Origin': 'https://bmis1.buildingmgt.gov.hk',
                         'Connection':'keep-alive',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                         'Host': 'bmis1.buildingmgt.gov.hk',
                         'Accept': 'application/xml, text/xml, */*; q=0.01',
                         'Referer': 'https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true'},
                formdata={'javax.faces.partial.ajax':'true',
                    'javax.faces.source':'_bld_result_frm:_result_tbl',
                    'javax.faces.partial.execute':'_bld_result_frm:_result_tbl',
                    'javax.faces.partial.render':'_bld_result_frm:_result_tbl',
                    'javax.faces.behavior.event':'page',
                    'javax.faces.partial.event':'page',
                    '_bld_result_frm:_result_tbl_pagination':'true',
                    '_bld_result_frm:_result_tbl_first':str(i * page_size),
                    '_bld_result_frm:_result_tbl_rows':str(page_size),
                    '_bld_result_frm:_result_tbl_encodeFeature':'true',
                    '_bld_result_frm:_result_tbl_columnOrder':'_bld_result_frm:_result_tbl:j_id_4c,_bld_result_frm:_result_tbl:j_id_4i,_bld_result_frm:_result_tbl:j_id_4o',
                    '_bld_result_frm_SUBMIT':'1',
                    'autoScroll':'',
                    'javax.faces.ViewState':view_state},
                meta={'cookiejar':response.meta['cookiejar'], 'view_state':view_state, 'page_index': response.meta['page_index'], 'page_size': response.meta['page_size']}, priority=1, dont_filter=True)


    def parse_first_page(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        span = soup.find_all("span", class_ ="ui-paginator-current")[0]
        total_text = "".join([str(x) for x in span.contents])
        print(total_text)
        pattern = '.*total[ ]+([0-9]*)[ ]+'
        m = re.match(pattern, total_text)
        total_numbers = int(m.group(1))
        page_size = 15
        total_pages = (total_numbers + page_size - 1) // page_size
        url = "https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true"
        for i in range(0, total_pages):
            yield scrapy.Request(url=url, callback=self.parse_view_state_page, meta={'cookiejar':i * 10, 'page_size': page_size, 'page_index': i}, priority=- 10 * i, dont_filter=True)
    

    def parse_page(self, response):
        soup = BeautifulSoup(response.body, "lxml-xml")
        html_body = soup.find_all("update", {"id": "_bld_result_frm:_result_tbl"})[0].contents[0]
        html_soup = BeautifulSoup(html_body, 'html.parser')
        for i, link in enumerate(html_soup.find_all('a')):
            if i % 2 == 1:
                continue
            print(link['id'])
            yield scrapy.FormRequest(url='https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf', 
                    dont_filter = True,
                    callback=self.parse_detail_page,
                    headers={'Accept-Encoding': 'gzip, deflate, br',
                             'X-Requested-With': 'XMLHttpRequest',
                             'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
                             'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                             'Origin': 'https://bmis1.buildingmgt.gov.hk',
                             'Connection':'keep-alive',
                             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                             'Host': 'bmis1.buildingmgt.gov.hk',
                             'Accept': 'application/xml, text/xml, */*; q=0.01',
                             'Referer': 'https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true',
                             'Upgrade-Insecure-Request': '1',
                             'Cache-Control': 'max-age=0'},
                    formdata={
                        '_bld_result_frm:_result_tbl_columnOrder':'_bld_result_frm:_result_tbl:j_id_4c,_bld_result_frm:_result_tbl:j_id_4i,_bld_result_frm:_result_tbl:j_id_4o',
                        '_bld_result_frm_SUBMIT':'1',
                        'autoScroll':'',
                        'javax.faces.ViewState':response.meta['view_state'],
                        link['id']:link['id']},
                    meta={'cookiejar':response.meta['cookiejar'], 'id':link['id']}, priority=100)
        i = response.meta['page_index']
        url = 'https://bmis1.buildingmgt.gov.hk/bd_hadbiex/content/searchbuilding/building_search.jsf?renderedValue=true'
        page_size = response.meta['page_size']

    def parse_detail_page(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        parent_div = soup.find('div', {'id': '_detail_form:j_id_2k_content'})
        output = {}
        for div in parent_div.find_all('div', {'class': 'col w2'}) + parent_div.find_all('div', {'class': 'col w1'}):
            label = div.find('div', {'class': 'label'}).text.strip()
            value = div.find('div', {'class': 'text'}).text.strip()
            output[label] = value
        k = 0
        for td in soup.find_all('td', {'role': 'gridcell'}):
            k = k + 1
            output["address_" + str(k)] = td.text.strip()
        organization_div = soup.find('div', {'id': '_detail_form:j_id_3r_content'})
        org_flattern = [org.text.strip() for org in organization_div.find_all('div', {'class': 'text'})]
        for i in range(0, len(org_flattern) // 2):
            output['org_type_' + str(i + 1)] = org_flattern[2 * i]
            output['org_name_' + str(i + 1)] = org_flattern[2 * i + 1]
        output['link_id'] = response.meta['id']
        yield output

