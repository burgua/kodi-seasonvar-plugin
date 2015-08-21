#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import urllib2


class SeasonvarWebOpener:

    __instance = None

    @staticmethod
    def __create_opener():
        web_opener = urllib2.build_opener()
        web_opener.addheaders.append(('Cookie', 'sva=lVe324PqsI24'))
        urllib2.install_opener(web_opener)
        return web_opener

    @staticmethod
    def __get_opener():
        # ToDo: singleton!
        if SeasonvarWebOpener._instance is None:
            _instance = SeasonvarWebOpener.__create_opener()
        return _instance

    @staticmethod
    def get_html(url):
        try:
            conn = SeasonvarWebOpener.__get_opener().open(url)
            html = conn.read()
            conn.close()
            return html
        except:
            # ToDo: failed!
            return None