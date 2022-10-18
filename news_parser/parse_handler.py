import time

import dateparser
import requests
from bs4 import BeautifulSoup

from models import ItemModel


class ResourceHandler():

    not_downloaded = []
    failed_resources = []

    def __call__(self, resource):
        news_url_list = self.parse_top(resource)
        if not news_url_list:
            return []
        news_content_list = self.parse_bottom(resource, news_url_list)
        return news_content_list

    def get_page(self, url):
        try:
            page = requests.get(url)
        except requests.exceptions.ConnectionError:
            return '!download_error'
        if page.status_code != 200:
            return '!download_error'
        page_as_soup_obj = BeautifulSoup(page.text, 'html.parser')
        return page_as_soup_obj

    def get_elements(self, page_as_soup_obj, tag_structure):
        tag = tag_structure[0]
        element_list = (page_as_soup_obj.find_all(tag, tag_structure[1]))
        return element_list

    def get_date(self, page, date_cut):
        date_element = self.get_elements(page, date_cut)[0]
        if 'datetime' in date_element.attrs:
            date = dateparser.parse(date_element.attrs['datetime'])
        else:
            date_data_list = date_element.text.split(',')
            date_to_parse = ','.join(date_data_list[1:])
            date = dateparser.parse(date_to_parse)
        nd_date = int(date.timestamp())
        not_date = date.strftime('%Y-%m-%d')
        return nd_date, not_date

    def parse_top(self, resource):
        news_url_list = []
        main_page = self.get_page(resource.resource_url)
        if main_page == '!download_error':
            ResourceHandler.failed_resources.append(resource.resource_url)
            return None
        news_list = self.get_elements(main_page, resource.top_tag)
        for news in news_list:
            if 'href' in news.attrs:
                news_url_list.append(news.attrs['href'])
        return news_url_list

    def parse_bottom(self, resource, url_list):
        news_content_list = []
        for url in url_list:
            page = self.get_page(url)
            if page == '!download_error':
                ResourceHandler.not_downloaded.append(url)
                continue
            news_item = ItemModel(
                res_id=resource.resource_id,
                link=url,
            )
            news_item.title = self.get_elements(
                page,
                resource.title_cut
            )[0].text
            news_item.content = str(
                self.get_elements(page, resource.bottom_tag)[0]
            )
            news_item.nd_date, news_item.not_date = self.get_date(
                page,
                resource.date_cut
            )
            news_item.s_date = int(time.time())
            news_content_list.append(news_item.formated_for_db())

        return news_content_list
