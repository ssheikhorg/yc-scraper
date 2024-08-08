import json

import scrapy


def make_start_urls_list() -> list:
    """Returns a list with the start urls."""
    with open('data/yc_links.txt', 'r') as f:
        return eval(f.read())


class YcspiderSpider(scrapy.Spider):
    name = "ycspider"
    allowed_domains = ["ycombinator.com"]
    start_urls = make_start_urls_list()

    def parse(self, response: scrapy.http.Response) -> dict:
        st = response.css('[data-page]::attr(data-page)').get()
        jo = json.loads(st)['props']
        data = jo['company']
        yield {
            'company_id': data['id'],
            'company_name': data['name'],
            'short_description': data['one_liner'],
            'long_description': data['long_description'],
            'batch': data['batch_name'],
            'status': data['ycdc_status'],
            'tags': data['tags'],
            'location': data['location'],
            'country': data['country'],
            'year_founded': data['year_founded'],
            'num_founders': len(data['founders']),
            'founders_names': [f['full_name'] for f in data['founders']],
            'team_size': data['team_size'],
            'website': data['website'],
            'cb_url': data['cb_url'],
            'linkedin_url': data['linkedin_url'],
        }
