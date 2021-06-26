import unittest

from document_template import DocumentTemplate, TemplateError


class CopyTestCase(unittest.TestCase):
    def setUp(self):
        print('setUp')
        dt = DocumentTemplate()
        self.dt = dt

    def test_copy_01(self):
        template_content = '''#{copy:start}1#{copy:end}'''
        id_dict = {
        }
        expect_content = '''1'''
        actual_content = self.dt.parse(template_content, id_dict)
        self.assertEqual(expect_content, actual_content)

    def test_copy_02(self):
        template_content = '''111##{copy:start}
        #{var1}#{var2}
        ##{copy:end}'''
        id_dict = {
            'var1': ['aaa', 'bbb', 'ccc'],
            'var2': ['xxx', 'yyy'],
        }
        expect_content = '''111#
        aaaxxx
        #
        bbbyyy
        #
        ccc
        #'''
        actual_content = self.dt.parse(template_content, id_dict)
        # print('actual_content', actual_content)
        self.assertEqual(expect_content, actual_content)

    def test_copy_03(self):
        template_content = '''#{copy:start}#{var1}111#{copy:end}222'''
        id_dict = {
            'var1': ['aaa', 'bbb', 'ccc'],
        }
        expect_content = '''aaa111bbb111ccc111222'''
        actual_content = self.dt.parse(template_content, id_dict)
        # print('actual_content', actual_content)
        self.assertEqual(expect_content, actual_content)

    def test_copy_04(self):
        template_content = '''#{copy:start}111'''
        id_dict = {
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 33)

    def test_copy_05(self):
        template_content = '''#{copy:}111'''
        id_dict = {
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 30)

    def test_copy_06(self):
        template_content = '''#{copy:end}111#{copy:start}'''
        id_dict = {
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 31)

    def test_copy_07(self):
        template_content = '''#{copy:a}111#{copy:end}'''
        id_dict = {
        }
        with self.assertRaises(TemplateError) as cm:
            self.dt.parse(template_content, id_dict)
        template_exception = cm.exception
        print(template_exception)
        self.assertEqual(template_exception.code, 32)

    def test_copy_08(self):
        template_content = '''#{copy:start}#{var1} #{copy:end} '''
        id_dict = {
        }
        expect_content = '''  '''
        actual_content = self.dt.parse(template_content, id_dict)
        # print('actual_content', actual_content)
        self.assertEqual(expect_content, actual_content)


if __name__ == '__main__':
    unittest.main()
