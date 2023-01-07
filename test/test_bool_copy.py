import unittest

from document_template import DocumentTemplate, TemplateError


class BoolCopyTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp')
        dt = DocumentTemplate()
        self.dt = dt

    def test_bool_copy_01(self):
        template_content = '''#{bool:var1}#{copy:start}111
        #{copy:end}
        #{bool:var1}'''

        # 1
        id_dict = {
            'var1': True,
        }
        expect_content = '''111
        
        '''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_01#1")

        # 2
        id_dict = {
            'var1': False,
        }
        expect_content = ''''''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_01#2")

        template_content = '''#{bool:!var1}#{copy:start}111
        #{copy:end}
        #{bool:!var1}'''

        # 3
        id_dict = {
            'var1': True,
        }
        expect_content = ''''''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_01#3")

        # 4
        id_dict = {
            'var1': False,
        }
        expect_content = '''111
        
        '''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_01#4")

    def test_bool_copy_02(self):
        template_content = '''111#{bool:var1}222#{bool:var2}
        #{copy:start}#{vara}#{copy:end}#{bool:var3}#{#{bool:var3}
        #{copy:start}#{varb}#{copy:end}
        #{bool:var2}#{bool:var1}'''

        # 1
        id_dict = {
            'var1': True,
            'var2': True,
            'var3': True,
            'vara': ['a', 'b', 'c'],
        }
        expect_content = '''111222
        abc#{
        
        '''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_02#1")

        # 2
        id_dict = {
            'var1': True,
            'var2': True,
            'var3': False,
            'vara': ['a', 'b', 'c'],
        }
        expect_content = '''111222
        abc
        
        '''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_02#2")

        # 3
        id_dict = {
            'var1': True,
            'var2': False,
            'var3': True,
            'vara': ['a', 'b', 'c'],
        }
        expect_content = '''111222'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_02#3")

        # 4
        id_dict = {
            'var1': False,
            'var2': True,
            'var3': True,
            'vara': ['a', 'b', 'c'],
        }
        expect_content = '''111'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_02#4")

        # 5
        id_dict = {
            'var1': False,
            'var2': False,
            'var3': False,
            'vara': ['a', 'b', 'c'],
        }
        expect_content = '''111'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content, "test_bool_copy_02#5")


if __name__ == '__main__':
    unittest.main()
