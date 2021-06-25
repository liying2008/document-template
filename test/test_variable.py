import unittest

from document_template import DocumentTemplate


class VariableTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp')
        dt = DocumentTemplate()
        self.dt = dt

    def test_variable_01(self):
        template_content = '''#{var1}#{var2}111
        222#{var3}333
        #{var4}'''
        id_dict = {
            'var1': 'aaa',
            'var2': 'bb',
            'var3': 'c',
            'var4': 'ddd',
        }
        expect_content = '''aaabb111
        222c333
        ddd'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_variable_02(self):
        template_content = '''111##{var1}
        #{var1#{var2}22#{{var1
        #{'''
        id_dict = {
            'var1': 'aaa',
            'var2': 'bb',
        }
        expect_content = '''111#aaa
        #{var1bb22#{{var1
        #{'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_variable_03(self):
        template_content = '''#{var1}'''
        id_dict = {
            'var1': 'aaa',
        }
        expect_content = '''aaa'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)


if __name__ == '__main__':
    unittest.main()
