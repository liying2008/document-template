#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from collections import Iterable

__author__ = 'liying'


class DocumentTemplate(object):
    def __init__(self):
        self.__template_file = None
        self.__identifier_dict = None

    def load(self, template_file):
        """加载模版文件"""
        if not os.path.isfile(template_file):
            raise ValueError("error! template_file does not exist.")
        else:
            self.__template_file = template_file

    def set_identifier_dict(self, identifier_dict):
        """设置标识符字典"""
        self.__identifier_dict = identifier_dict

    def get_document(self):
        """获取解析后的文档"""
        if self.__template_file is None:
            raise ValueError("error! no template_file.")
        if self.__identifier_dict is None:
            raise ValueError("error! no identifier_dict")
        document = ""
        with open(self.__template_file, 'r') as f:
            for line in f:
                start_pos = line.find("#{")
                while start_pos >= 0:
                    if line[start_pos + 2:start_pos + 7] == "bool:":
                        right_brace_pos = line.find("}", start_pos + 8)
                        if right_brace_pos > start_pos:
                            identifier = line[start_pos + 7:right_brace_pos]
                            next_start_pos = line.find("#{bool:" + identifier + "}", start_pos + 8)
                            if next_start_pos > right_brace_pos:
                                if self.__identifier_dict[identifier]:
                                    line = line[0:start_pos] + line[right_brace_pos + 1:next_start_pos] + \
                                           line[next_start_pos + right_brace_pos - start_pos + 1:]
                                else:
                                    line = line[0:start_pos] + line[next_start_pos + right_brace_pos - start_pos + 1:]
                        start_pos = line.find("#{")
                    elif line[start_pos + 2:start_pos + 13] == "copy:start}":
                        next_start_pos = line.find("#{copy:end}", start_pos + 14)
                        if next_start_pos > start_pos:
                            content = line[start_pos + 13:next_start_pos]
                            content_start_pos = content.find("#{")
                            if content_start_pos > 0:
                                content_right_brace_pos = content.find("}", content_start_pos + 3)
                                if content_right_brace_pos > content_start_pos:
                                    content_identifier = content[content_start_pos + 2:content_right_brace_pos]
                                    if isinstance(self.__identifier_dict[content_identifier], basestring):
                                        line = line[0:start_pos] + content[0:content_start_pos] + \
                                               self.__identifier_dict[content_identifier] + \
                                               content[content_right_brace_pos + 1:] + line[next_start_pos + 11:]
                                    elif isinstance(self.__identifier_dict[content_identifier], Iterable):
                                        line_satrt = line[0:start_pos]
                                        line_end = line[next_start_pos + 11:]
                                        line = line_satrt
                                        content_start = content[0:content_start_pos]
                                        content_end = content[content_right_brace_pos + 1:]
                                        for c in self.__identifier_dict[content_identifier]:
                                            line += content_start + c + content_end
                                        line += line_end
                        start_pos = line.find("#{")
                    else:
                        end_pos = line.find("}", start_pos + 1)
                        if end_pos > start_pos:
                            line = line[0:start_pos] + self.__identifier_dict[line[start_pos + 2:end_pos]] + \
                                   line[end_pos + 1:]
                        start_pos = line.find("#{")
                document += line
        return document

    def save_document(self, new_file):
        """保存到文件"""
        document = self.get_document()
        with open(new_file, 'w') as f:
            f.write(document)
