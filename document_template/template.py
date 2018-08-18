#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import os

__author__ = 'liying'


class DocumentTemplate(object):
    def __init__(self):
        self.__template_file = None
        self.__identifier_dict = None
        self.__encoding = 'utf-8'

    def load(self, template_file, encoding='utf-8'):
        """加载模版文件"""
        if not os.path.isfile(template_file):
            raise ValueError("error! template_file does not exist.")
        else:
            self.__template_file = template_file
            self.__encoding = encoding

    def set_identifier_dict(self, identifier_dict):
        """设置标识符字典"""
        self.__identifier_dict = identifier_dict

    def __fill_list(self, dict_key_list):
        """取同一行所含 list 中的最大长度，并将长度小的 list 补至最大长度"""
        key_len = len(dict_key_list)
        list_max_length = 0
        for i in range(key_len):
            length = len(self.__identifier_dict[dict_key_list[i]])
            if length > list_max_length:
                list_max_length = length

        for i in range(key_len):
            a_list = self.__identifier_dict[dict_key_list[i]]
            short = list_max_length - len(a_list)
            if short > 0:
                self.__identifier_dict[dict_key_list[i]] = list(self.__identifier_dict[dict_key_list[i]])
                for j in range(short):
                    self.__identifier_dict[dict_key_list[i]].append('')
        return list_max_length

    def get_document(self):
        """获取解析后的文档"""
        if self.__template_file is None:
            raise ValueError("error! no template_file.")
        if self.__identifier_dict is None:
            raise ValueError("error! no identifier_dict")
        document = ""
        with codecs.open(self.__template_file, 'r', encoding=self.__encoding) as f:
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
                            # 一行中的变量标识符列表
                            identifier_list = []
                            # 一行中的正常文字列表
                            middle_text = []
                            content = line[start_pos + 13:next_start_pos]
                            content_start_pos = content.find("#{")
                            # 找到所有的变量标识符和正常文字
                            while content_start_pos > 0:
                                content_right_brace_pos = content.find("}", content_start_pos + 3)
                                if content_right_brace_pos > content_start_pos:
                                    content_identifier = content[content_start_pos + 2:content_right_brace_pos]
                                    identifier_list.append(content_identifier)
                                    middle_text.append(content[0:content_start_pos])
                                    content = content[content_right_brace_pos + 1:next_start_pos]
                                    content_start_pos = content.find("#{")

                            middle_text.append(content)

                            identifier_count = len(identifier_list)
                            if identifier_count > 0:
                                line = ''
                                length = self.__fill_list(identifier_list)
                                for i in range(length):
                                    for j in range(identifier_count):
                                        line += middle_text[j] + self.__identifier_dict[identifier_list[j]][i]
                                    line += middle_text[identifier_count]

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
        with codecs.open(new_file, 'w', encoding=self.__encoding) as f:
            f.write(document)
