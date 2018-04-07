#!/usr/bin/python
# -*- coding: utf-8 -*-

from template import DocumentTemplate

__author__ = 'liying'

if __name__ == '__main__':
    id_dict = {"title": "标题", "head": "正文标题", "url": "https://github.com/liying2008", "large_font": "大号字体"}
    id_dict['show_span'] = True
    # id_dict['contents'] = 'Hello World'
    id_dict['contents'] = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    temp = DocumentTemplate()
    temp.load("test.html")
    temp.set_identifier_dict(id_dict)
    temp.save_document("new_test.html")
