#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json


class SeasonvarWebOpener:

    __instance = None

    def __init__(self):
        return

    @staticmethod
    def __create_opener():
        web_opener = urllib2.build_opener()
        web_opener.addheaders.append(('Cookie', 'sva=lVe324PqsI24'))
        urllib2.install_opener(web_opener)
        return web_opener

    def __get_opener(self):
        if self.__instance is None:
            self.__instance = SeasonvarWebOpener.__create_opener()
        return self.__instance

    def get_json(self, url):
        response = self.get_html(url)
        return json.loads(response)

    def get_html(self, url):
        try:
            conn = self.__get_opener().open(url)
            html = conn.read()
            conn.close()
            return html
        except:
            return None
