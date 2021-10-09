import requests
import scrapy
from datetime import datetime


class RegelleistungSpider(scrapy.Spider):
    name = 'regelleistung'
    allowed_domains = ['regelleistung.net']
    start_urls = ['https://www.regelleistung.net/ext/data/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36'  # noqa
    }

    tso_ids = {
        '50Hertz': '4',
        'Amprion': '3',
        'TenneT': '2',
        'TransnetBW': '1',
        'Netzregelverbund': '6',
        'IGCC': '11',
        'Netzregelverbund detailliert': '-42'
    }

    def parse(self, response):
        today = datetime.today()
        date_str = today.strftime('%d.%m.%Y')

        # for tso_key, tso_value in self.tso_ids.items():
        #     # get list of data types for tso
        #     resp = requests.get(f"https://www.regelleistung.net/ext/data/products?uenbId={tso_value}")
        #     if resp.status_code == 200:
        #         resp_data = resp.json()
        #         for data_type_key, data_type_value in resp_data.items():
        #             return scrapy.FormRequest.from_response(
        #                 response,
        #                 method='POST',
        #                 formid='search-for-data',
        #                 formdata={'from': date_str, '_download': 'on', 'tsoId': tso_value, 'dataType': data_type_value},
        #                 callback=self.search_result
        #             )
        return scrapy.FormRequest.from_response(
            response,
            method='POST',
            formid='search-for-data',
            formdata={'from': date_str, '_download': 'on', 'tsoId': '11', 'dataType': 'AUSTAUSCH_CH'},
            callback=self.search_result
        )

    def search_result(self, response):
        table = response.xpath('//*[@id="data-table"]')
        rows = response.xpath('//*[@id="data-table"]//tbody//tr')
        for row in rows:

            item = {
                'date': self.get_date(row),
                'time_from': self.get_time_from(row),
                'time_to': self.get_time_to(row),
                'betr_neg_[MW]': self.get_betr_neg_mw(row),
                'betr_pos_[MW]': self.get_betr_pos_mw(row),
                'qual_neg_[MW]': self.get_qual_neg_mw(row),
                'qual_pos_[MW]': self.get_betr_pos_mw(row)
            }

            yield item
    
    def get_date(self, row):
        try:
            result = row.xpath('td//text()')[0].extract()
        except Exception as exc:
            result = ''
        return result
    
    def get_time_from(self, row):
        try:
            result = row.xpath('td//text()')[1].extract()
        except Exception as exc:
            result = ''
        return result
    
    def get_time_to(self, row):
        try:
            result = row.xpath('td//text()')[2].extract()
        except Exception as exc:
            result = ''
        return result
    
    def get_betr_neg_mw(self, row):
        try:
            result = row.xpath('td//text()')[3].extract()
        except Exception as exc:
            result = ''
        return result
    
    def get_betr_pos_mw(self, row):
        try:
            result = row.xpath('td//text()')[4].extract()
        except Exception as exc:
            result = ''
        return result
    
    def get_qual_neg_mw(self, row):
        try:
            result = row.xpath('td//text()')[5].extract()
        except Exception as exc:
            result = ''
        return result
    
    def get_qual_pos_(self, row):
        try:
            result = row.xpath('td//text()')[6].extract()
        except Exception as exc:
            result = ''
        return result
    
