#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

__author__ = 'liying'


class Template:
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
                if "#{" in line:
                    for key, value in self.__identifier_dict.items():
                        line = line.replace("#{" + key + "}", value)
                        if "#{" not in line:
                            break
                document += line
        return document

    def save_document(self, new_file):
        """保存到文件"""
        document = self.get_document()
        with open(new_file, 'w') as f:
            f.write(document)
