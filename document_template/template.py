# -*- coding: utf-8 -*-

import codecs
import os

__author__ = 'liying'


class TemplateError(Exception):
    """Template error."""

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'error code = ' + str(self.code) + ', ' + self.message


class IdentifierError(Exception):
    """Identifier error."""

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'error code = ' + str(self.code) + ', ' + self.message


class DocumentTemplate(object):
    def __init__(self):
        self.__template_content = None
        self.__identifier_dict = None

    def load(self, template_file, encoding='utf-8'):
        """
        Read template content from file.

        :param template_file: template file.
        :param encoding: specifies the encoding which is to be used for the file.
        """
        if not os.path.isfile(template_file):
            raise TemplateError(code=1, message="template file does not exist or is not a file.")

        with codecs.open(template_file, 'r', encoding=encoding) as f:
            self.__template_content = f.read()

    def load_template_content(self, template_content):
        """
        Load template content.

        :param template_content: template content.
        """
        self.__template_content = template_content

    def set_identifier_dict(self, identifier_dict):
        """
        Set the identifier dict.

        :param identifier_dict: identifier dict.
        """
        self.__identifier_dict = identifier_dict

    def get_document(self):
        """
        Get the parsed document.

        :return: The parsed document.
        """
        if self.__template_content is None:
            raise TemplateError(code=2, message="template file or template content is not set.")
        if self.__identifier_dict is None:
            raise IdentifierError(code=1, message="identifier dict is not set.")
        document = ""

        template_content = self.__template_content
        char_count = len(template_content)
        # print('char_count=' + str(char_count))

        # 跳过次数
        skip_count = 0

        bool_flags = {}
        # struct
        # {
        #     "var1": {
        #         "start_index": 12,
        #         "negation": False,
        #         "content": "",
        #     },
        #     "var2": {
        #         "start_index": 11,
        #         "negation": True,
        #         "content": "test",
        #     }
        # }

        # bool 指令变量 栈
        bool_flags_stack = []

        for i in range(char_count):
            if skip_count > 0:
                skip_count -= 1
                continue
            if i < char_count - 2 and template_content[i] == '#' and template_content[i + 1] == '{':
                right_bracket_index = self.__get_next_right_bracket(template_content[i + 2:])
                # print('right_bracket_index=' + str(right_bracket_index))
                if right_bracket_index == -1:
                    # 没有 }
                    if len(bool_flags_stack) == 0:
                        # 没有 bool 指令要处理
                        document += '#{'
                    else:
                        # 还有 bool 指令要处理
                        last_bool_var = bool_flags_stack[len(bool_flags_stack) - 1]
                        bool_flags[last_bool_var]['content'] += '#{'

                    skip_count = 1
                    continue
                else:
                    # #{temp_var}
                    temp_var = template_content[i + 2:i + 2 + right_bracket_index]
                    # print('temp_var=' + temp_var)
                    colon_index = temp_var.find(':')
                    if colon_index == -1:
                        # 普通变量
                        value = self.__identifier_dict.get(temp_var, '')
                        # print('value=' + value)
                        if len(bool_flags_stack) == 0:
                            # 没有 bool 指令要处理
                            document += value
                        else:
                            # 还有 bool 指令要处理
                            last_bool_var = bool_flags_stack[len(bool_flags_stack) - 1]
                            bool_flags[last_bool_var]['content'] += value

                        skip_count = 2 + right_bracket_index
                        continue
                    else:
                        if temp_var[0:colon_index] == 'bool':
                            # bool 指令变量
                            var = temp_var[colon_index + 1:]
                            if var == '':
                                # bool 变量为空，抛出异常
                                raise TemplateError(code=20, message='bool variable is empty.')
                            else:
                                negation = False
                                if var[0] == '!':
                                    negation = True
                                    var = var[1:]
                                if var in bool_flags:
                                    origin_negation = bool_flags[var]['negation']
                                    content = bool_flags[var]['content']
                                    del bool_flags[var]
                                    pop_var = bool_flags_stack.pop()
                                    if pop_var != var:
                                        # bool 指令嵌套错误
                                        raise TemplateError(code=21, message='bool directive nesting error.')
                                    if negation != origin_negation:
                                        # bool 指令取反状态前后不一致
                                        raise TemplateError(code=23,
                                                            message='bool directive negations do not match before and after.')
                                    if self.__identifier_dict.get(var, False) != origin_negation:
                                        # bool 内容显示
                                        if len(bool_flags_stack) != 0:
                                            # 还有 bool 指令未处理完毕
                                            last_var = bool_flags_stack[len(bool_flags_stack) - 1]
                                            bool_flags[last_var]['content'] += content
                                        else:
                                            # 所有 bool 指令处理完毕
                                            document += content
                                    else:
                                        # bool 内容不显示
                                        # nothing to do
                                        pass
                                else:
                                    bool_flags[var] = {
                                        'start_index': i,
                                        'negation': negation,
                                        'content': ""
                                    }
                                    # print('var', var, 'bool_flags', bool_flags)
                                    bool_flags_stack.append(var)
                                # 当前 bool 指令解析完毕
                                skip_count = 2 + right_bracket_index
                                continue
                        elif temp_var[0:colon_index] == 'copy':
                            # copy 标记
                            flag = temp_var[colon_index + 1:]
                            if flag == '':
                                raise TemplateError(code=30,
                                                    message='copy directive flag cannot be empty, it should be "start" or "end".')
                            elif flag == 'end':
                                raise TemplateError(code=31,
                                                    message='copy directive flag should appear first as "start" and then as "end".')
                            elif flag != 'start':
                                raise TemplateError(code=32,
                                                    message='copy directive flag can only be "start" or "end".')
                            else:
                                # flag is start
                                copy_end_index = self.__find_copy_end_index(
                                    template_content[i + 2 + right_bracket_index:])
                                if copy_end_index == -1:
                                    raise TemplateError(code=33, message='missing #{copy:end} .')
                                else:
                                    copy_content = template_content[
                                                   i + 3 + right_bracket_index:i + 2 + right_bracket_index + copy_end_index]
                                    value = self.__deal_copy(copy_content)
                                    if len(bool_flags_stack) == 0:
                                        # 没有 bool 指令要处理
                                        document += value
                                    else:
                                        # 还有 bool 指令要处理
                                        last_bool_var = bool_flags_stack[len(bool_flags_stack) - 1]
                                        bool_flags[last_bool_var]['content'] += value
                                    # copy 指令处理完毕（处理了一对 copy 指令）
                                    # +10 是用来跳过 #{copy:end} 这些字符
                                    skip_count = 2 + right_bracket_index + copy_end_index + 10
                                    continue

                        else:
                            # 不支持的标记，原样输出
                            if len(bool_flags_stack) == 0:
                                # 没有 bool 指令要处理
                                document += '#{' + temp_var + '}'
                            else:
                                # 还有 bool 指令要处理
                                last_bool_var = bool_flags_stack[len(bool_flags_stack) - 1]
                                bool_flags[last_bool_var]['content'] += '#{' + temp_var + '}'

                            skip_count = 2 + right_bracket_index
                            continue

            else:
                if len(bool_flags_stack) == 0:
                    # 没有 bool 指令要处理
                    document += template_content[i]
                else:
                    # 还有 bool 指令要处理
                    last_bool_var = bool_flags_stack[len(bool_flags_stack) - 1]
                    bool_flags[last_bool_var]['content'] += template_content[i]

        if len(bool_flags_stack) > 0:
            # bool 指令未完整配对
            raise TemplateError(code=22, message='bool directive pairing error.')

        return document

    def save_document(self, new_file, encoding='utf-8'):
        """
        Save the parsed document to a file.

        :param new_file: filename.
        :param encoding: specifies the encoding which is to be used for the file.
        """
        document = self.get_document()
        with codecs.open(new_file, 'w', encoding=encoding) as f:
            f.write(document)

    def parse(self, template_content, identifier_dict):
        """
        Parse the template content and generate the processed content.

        :param template_content: template content.
        :param identifier_dict: identifier dict.
        :return: the processed content.
        """
        self.__template_content = template_content
        self.__identifier_dict = identifier_dict
        return self.get_document()

    @staticmethod
    def __get_next_right_bracket(text):
        """获取 } 的位置"""
        index = -1
        for char in text:
            if '0' <= char <= '9' or 'a' <= char <= 'z' or 'A' <= char <= 'Z' or char == '_' or char == ':' or char == '!':
                index += 1
            elif char == '}':
                index += 1
                break
            else:
                index = -1
                break

        return index

    @staticmethod
    def __find_copy_end_index(text):
        return text.find('#{copy:end}')

    def __deal_copy(self, content):
        """处理 copy 指令"""
        # print('deal_content=' + content)
        final_content = ''
        loop_count = 1
        temp_content = content
        while temp_content != '':
            start_flag_index = temp_content.find('#{')
            if start_flag_index == -1:
                final_content += temp_content
                temp_content = ''

            final_content += temp_content[0:start_flag_index]
            end_flag_index = temp_content.find('}', start_flag_index + 2)
            if end_flag_index == -1:
                # 没有 } ，把 #{... 当做普通字符串处理，原样输出
                final_content += temp_content[start_flag_index:]
                temp_content = ''
            else:
                var = temp_content[start_flag_index + 2:end_flag_index]
                collection = self.__identifier_dict.get(var, [''])
                if len(collection) > loop_count:
                    loop_count = len(collection)
                final_content += collection[0]
                temp_content = temp_content[end_flag_index + 1:]

        # print('loop_count=' + str(loop_count))

        for i in range(1, loop_count):
            temp_content = content
            while temp_content != '':
                start_flag_index = temp_content.find('#{')
                if start_flag_index == -1:
                    final_content += temp_content
                    temp_content = ''

                final_content += temp_content[0:start_flag_index]
                end_flag_index = temp_content.find('}', start_flag_index + 2)
                if end_flag_index == -1:
                    # 没有 } ，把 #{... 当做普通字符串处理，原样输出
                    final_content += temp_content[start_flag_index:]
                    temp_content = ''
                else:
                    var = temp_content[start_flag_index + 2:end_flag_index]
                    collection = self.__identifier_dict.get(var, [''])
                    if len(collection) > i:
                        final_content += collection[i]
                    temp_content = temp_content[end_flag_index + 1:]

        return final_content
