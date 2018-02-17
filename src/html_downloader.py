#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request


class HTMLDownloader(object):
    
    @staticmethod
    def download(url):
        if url is None:
            return None

        response = urllib.request.urlopen(url)

        if response.getcode() != 200:
            return None

        return response.read().decode('utf-8', 'ignore')
