=====================
document-template
=====================

Python解析文档模版
=====================
     
.. image:: https://img.shields.io/pypi/v/document-template.svg
    :target: https://pypi.org/project/document-template/
.. image:: https://img.shields.io/pypi/pyversions/document-template.svg
    :target: https://pypi.org/project/document-template/
.. image:: https://img.shields.io/pypi/l/document-template.svg
    :target: https://github.com/liying2008/document-template
.. image:: https://img.shields.io/pypi/wheel/document-template.svg
    :target: https://pypi.org/project/document-template/#files


安装方法
---------
使用 **pip** 安装：
::

    pip install document-template

使用方法
---------
参考 test.py_  和 test.html_ :

.. _test.py: https://github.com/liying2008/document-template/blob/master/test.py
.. _test.html: https://github.com/liying2008/document-template/blob/master/test.html

:test.html:

.. code-block:: html

    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
            content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>#{title}</title>
    </head>
    <body>
    <h1>#{head}</h1>
    <a href="#{url}">#{url}</a>
    <br>
    Test.......
    <hr>
    <span style="font-size: larger;font-weight: bold">#{large_font}</span>
    <br>
    为真时显示:#{bool:show_span}<span>显示的内容</span>#{bool:show_span};;分割;;#{bool:show_span}show_span is True#{bool:show_span}
    <br>
    #{copy:start}多行文字，替换局部内容：#{contents} 和 #{another_contents}<br>#{copy:end}
    </body>
    </html>


:test.py:

.. code-block:: python

    from template import DocumentTemplate

    if __name__ == '__main__':
        id_dict = {"title": "标题", "head": "正文标题", "url": "https://github.com/liying2008", "large_font": "大号字体"}
        id_dict['show_span'] = True
        # id_dict['contents'] = 'ABCDEFG'
        # id_dict['another_contents'] = '1234567'
        id_dict['contents'] = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
        id_dict['another_contents'] = ('1', '2', '3', '4', '5', '6', '7')
        temp = DocumentTemplate()
        temp.load("test.html", encoding='utf-8')
        temp.set_identifier_dict(id_dict)
        temp.save_document("new_test.html")


注意事项
---------
- 成对出现的 **#{bool:}** 须在同一行；
- 成对出现的 **#{copy:}** 须在同一行；
- 不支持 **#{bool:}**、 **#{copy:}** 嵌套使用。


LICENSE
---------
`MIT License <https://github.com/liying2008/document-template/blob/master/LICENSE>`_

