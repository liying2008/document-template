import unittest

from document_template import DocumentTemplate, TemplateError


class BoolVariableTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp')
        dt = DocumentTemplate()
        self.dt = dt

    def test_bool_variable_01(self):
        template_content = '''#{bool:var1}111
        #{bool:var1}#{vara}'''

        # 1
        id_dict = {
            'var1': True,
            'vara': 'aaa'
        }
        expect_content = '''111
        aaa'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 2
        id_dict = {
            'var1': False,
            'vara': 'aaa'
        }
        expect_content = '''aaa'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_bool_variable_02(self):
        template_content = '''#{vara}#{bool:var1}#{varb}#{bool:var2}
        #{varc}#{bool:var3}#{#{bool:var3}444
        #{bool:var2}#{bool:var1}'''

        # 1
        id_dict = {
            'var1': True,
            'var2': True,
            'var3': True,
            'vara': '111',
            'varb': '222',
            'varc': '333',
        }
        expect_content = '''111222
        333#{444
        '''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 2
        id_dict = {
            'var1': True,
            'var2': True,
            'var3': False,
            'vara': '111',
            'varb': '222',
            'varc': '333',
        }
        expect_content = '''111222
        333444
        '''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 3
        id_dict = {
            'var1': True,
            'var2': False,
            'var3': True,
            'vara': '111',
            'varb': '222',
            'varc': '333',
        }
        expect_content = '''111222'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 4
        id_dict = {
            'var1': False,
            'var2': True,
            'var3': True,
            'vara': '111',
            'varb': '222',
            'varc': '333',
        }
        expect_content = '''111'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 5
        id_dict = {
            'var1': False,
            'var2': False,
            'var3': False,
            'vara': '111',
            'varb': '222',
            'varc': '333',
        }
        expect_content = '''111'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_bool_variable_03(self):
        template_content = '''#{vara}#{bool:}#{bool:}'''
        id_dict = {
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 20)

    def test_bool_variable_04(self):
        template_content = '''111#{bool:var1}#{vara}222'''
        id_dict = {
            "var1": False
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 22)

    def test_bool_variable_05(self):
        template_content = '''111#{bool:var1}#{vara}#{bool:var2}
        #{bool:var1}#{bool:var2}'''
        id_dict = {
            "var1": False
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 21)


if __name__ == '__main__':
    unittest.main()
