#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from document_template import DocumentTemplate

__author__ = 'liying'

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    id_dict = {"title": "标题", "head": "正文标题", "url": "https://github.com/liying2008", "large_font": "大号字体"}
    id_dict['show_span'] = True

    # Multi-line copy supports string, list and tuple
    # id_dict['contents'] = 'ABCDEFG'
    # id_dict['another_contents'] = '1234567'
    id_dict['contents'] = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    id_dict['another_contents'] = ['1', '2', '3', '4', '5', '6', '7']
    dt = DocumentTemplate()
    dt.load("test.html", encoding='utf-8')
    dt.set_identifier_dict(id_dict)
    dt.save_document("new_test.html")
