#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Here the translation from user input to safe html must be provided,however it's not provided. The easiest
    replacements are made just.
"""
import re

def input_to_safe_html(content):
    content = unicode(content)
    content = content.replace('<', u'&lt')
    content = content.replace('>', u'&gt')
    return content


def input_to_extended_safe_html (content):
        content = input_to_safe_html(content)
        content = content.replace ('&ltb&gt','<b>')
        content = content.replace ('&lt/b&gt','</b>')
        content = content.replace ('&lti&gt','<i>')
        content = content.replace ('&lt/i&gt','</i>')
        #content = content.replace(' ', u'&nbsp')
        ############link replacement
        pat1 = re.compile(r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", 
                            re.IGNORECASE | re.DOTALL)
        #pat2 = re.compile(r"#(^|[\n ])(((www|ftp)\.[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)", 
        #                       re.IGNORECASE | re.DOTALL)
        #urlstr = 'http://www.example.com/foo/bar.html'
        content = pat1.sub(r'\1<a href="\2" target="_blank">\3</a>', content)
        #content = pat2.sub(r'\1<a href="\2" target="_blank">\3</a>', content)
        content = content.replace('\n', '<br>')
        return content