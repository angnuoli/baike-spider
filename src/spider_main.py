# -*- coding: utf-8 -*-
import url_manager, html_parser, html_downloader, html_outputer
from urllib.request import quote, unquote
import argparse

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HTMLDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, url, max_num):
        self.urls.add_new_url(url)
        count = 1
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('craw {:d} : {}'.format(count, unquote(new_url)))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == max_num:
                    break
                count = count + 1
            except:
                print("craw failer")

        self.outputer.output_html()

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("baike_entry", type=str, help="Input a string as the baike entry which you want to search.")
    parse.add_argument("entry_max_num", type=int, help="The maximum of related pages. The range is [0, 100].")
    args = parse.parse_args()
    root_url = "https://baike.baidu.com/item/" + quote(args.baike_entry)
    obj_spider = SpiderMain()
    obj_spider.craw(root_url, min(100, max(0, args.entry_max_num)))
