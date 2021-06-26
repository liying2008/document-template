import unittest

from document_template import DocumentTemplate, TemplateError


class BoolCopyVariableTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp')
        dt = DocumentTemplate()
        self.dt = dt

    def test_bool_copy_variable_01(self):
        template_content = '''#{bool:var1}#{copy:start}111
        #{copy:end}#{varx}
        #{bool:var1}#{vary}'''

        # 1
        id_dict = {
            'var1': True,
            'varx': '222',
            'vary': '333',
        }
        expect_content = '''111
        222
        333'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 2
        id_dict = {
            'var1': False,
            'varx': '222',
            'vary': '333',
        }
        expect_content = '''333'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_bool_copy_variable_02(self):
        template_content = '''111#{bool:var1}222#{bool:var2}
        #{copy:start}#{vara}#{copy:end}#{bool:var3}#{#{bool:var3}
        #{copy:start}#{varb}#{copy:end}#{varx}
        #{bool:var2}#{bool:var1}#{vary}'''

        # 1
        id_dict = {
            'var1': True,
            'var2': True,
            'var3': True,
            'vara': ['a', 'b', 'c'],
            'varx': '444',
            'vary': '555',
        }
        expect_content = '''111222
        abc#{
        444
        555'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 2
        id_dict = {
            'var1': True,
            'var2': True,
            'var3': False,
            'vara': ['a', 'b', 'c'],
            'varx': '444',
            'vary': '555',
        }
        expect_content = '''111222
        abc
        444
        555'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 3
        id_dict = {
            'var1': True,
            'var2': False,
            'var3': True,
            'vara': ['a', 'b', 'c'],
            'varx': '444',
            'vary': '555',
        }
        expect_content = '''111222555'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 4
        id_dict = {
            'var1': False,
            'var2': True,
            'var3': True,
            'vara': ['a', 'b', 'c'],
            'varx': '444',
            'vary': '555',
        }
        expect_content = '''111555'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 5
        id_dict = {
            'var1': False,
            'var2': False,
            'var3': False,
            'vara': ['a', 'b', 'c'],
            'varx': '444',
            'vary': '555',
        }
        expect_content = '''111555'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)


if __name__ == '__main__':
    unittest.main()
