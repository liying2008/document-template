#!/usr/bin/python
# -*- coding: utf-8 -*-

from template import Template

__author__ = 'liying'

if __name__ == '__main__':
    id_dict = {"title": "标题", "head": "正文标题", "url": "https://github.com/liying2008", "large_font": "大号字体"}
    temp = Template()
    temp.load("test.html")
    temp.set_identifier_dict(id_dict)
    temp.save_document("new_test.html")
