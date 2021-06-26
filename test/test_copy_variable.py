import unittest

from document_template import DocumentTemplate, TemplateError


class CopyVariableTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp')
        dt = DocumentTemplate()
        self.dt = dt

    def test_copy_variable_01(self):
        template_content = '''#{vara}#{copy:start}1#{copy:end}'''
        id_dict = {
            "vara": "222"
        }
        expect_content = '''2221'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_copy_variable_02(self):
        template_content = '''111##{copy:start}
        #{var1}#{var2}
        ##{copy:end}#{vara}'''
        id_dict = {
            'var1': ['aaa', 'bbb', 'ccc'],
            'var2': ['xxx', 'yyy'],
            'vara': '222'
        }
        expect_content = '''111#
        aaaxxx
        #
        bbbyyy
        #
        ccc
        #222'''
        actual_content = self.dt.parse(template_content, id_dict)
        # print('actual_content', actual_content)
        self.assertEqual(expect_content, actual_content)

    def test_copy_variable_03(self):
        template_content = '''#{copy:start}#{var1}111#{copy:end}222#{vara}444'''
        id_dict = {
            'var1': ['aaa', 'bbb', 'ccc'],
            "vara": "333"
        }
        expect_content = '''aaa111bbb111ccc111222333444'''
        actual_content = self.dt.parse(template_content, id_dict)
        # print('actual_content', actual_content)
        self.assertEqual(expect_content, actual_content)

    def test_copy_variable_04(self):
        template_content = '''#{vara}#{copy:start}#{varb}'''
        id_dict = {
            "vara": "111",
            "varb": "222",
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 33)

    def test_copy_variable_05(self):
        template_content = '''#{vara}#{copy:}#{varb}'''
        id_dict = {
            "vara": "111",
            "varb": "222",
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 30)

    def test_copy_variable_06(self):
        template_content = '''#{vara}#{copy:end}111#{copy:start}#{varb}'''
        id_dict = {
            "vara": "111",
            "varb": "222",
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 31)

    def test_copy_variable_07(self):
        template_content = '''#{vara}#{copy:a}111#{copy:end}#{varb}'''
        id_dict = {
            "vara": "111",
            "varb": "222",
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 32)

    def test_copy_variable_08(self):
        template_content = '''#{vara}#{copy:start}#{var1} #{copy:end} #{varb} '''
        id_dict = {
            "vara": "111",
            "varb": "222",
        }
        expect_content = '''111  222 '''
        actual_content = self.dt.parse(template_content, id_dict)
        # print('actual_content', actual_content)
        self.assertEqual(expect_content, actual_content)


if __name__ == '__main__':
    unittest.main()
