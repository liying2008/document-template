import unittest

from document_template import DocumentTemplate, TemplateError


class BoolTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp')
        dt = DocumentTemplate()
        self.dt = dt

    def test_bool_01(self):
        template_content = '''#{bool:var1}111
        #{bool:var1}'''

        # 1
        id_dict = {
            'var1': True,
        }
        expect_content = '''111
        '''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 2
        id_dict = {
            'var1': False,
        }
        expect_content = ''''''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_bool_02(self):
        template_content = '''111#{bool:var1}222#{bool:var2}
        333#{bool:var3}#{#{bool:var3}444
        #{bool:var2}#{bool:var1}'''

        # 1
        id_dict = {
            'var1': True,
            'var2': True,
            'var3': True,
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
        }
        expect_content = '''111222'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 4
        id_dict = {
            'var1': False,
            'var2': True,
            'var3': True,
        }
        expect_content = '''111'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

        # 5
        id_dict = {
            'var1': False,
            'var2': False,
            'var3': False,
        }
        expect_content = '''111'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_bool_03(self):
        template_content = '''#{bool:}#{bool:}'''
        id_dict = {
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 20)

    def test_bool_04(self):
        template_content = '''111#{bool:var1}222'''
        id_dict = {
            "var1": False
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 22)

    def test_bool_05(self):
        template_content = '''111#{bool:var1}222#{bool:var2}
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
