#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import urllib.parse as urlparse

from bs4 import BeautifulSoup


class HtmlParser(object):
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    @staticmethod
    def _get_new_urls(page_url, soup) -> set:
        new_urls = set()
        # /item/***
        links = soup.find_all('a', href=re.compile(r"/item/.*"))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    @staticmethod
    def _get_new_data(page_url, soup) -> {}:
        # url
        res_data = {'url': urlparse.unquote
        (page_url)}

        # title
        # <dd class="lemmaWgt-lemmaTitle-title" _vimium-has-onclick-listener=""><h1>***</h1></dd>
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')
        res_data['title'] = title_node.get_text()

        # summary
        # <div class="lemma-summary" label-module="lemmaSummary" _vimium-has-onclick-listener="">***</div>
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()

        return res_data
