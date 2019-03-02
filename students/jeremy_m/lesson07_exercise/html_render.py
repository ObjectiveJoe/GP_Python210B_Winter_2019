#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element(object):
    tag = 'html'

    def __init__(self, contents=None, **kwargs):
        if contents:
            self.contents = [contents]
        else:
            self.contents = []

        self.kwargs = kwargs

    def append(self, new_content):
        self.contents.append(new_content)

    def render(self, out_file):
        if self.kwargs:
            self.render_kwargs(out_file)
            out_file.write(">\n")
        else:
            out_file.write("<{}>\n".format(self.tag))

        self.render_content(out_file)

        out_file.write('\n')
        out_file.write("</{}>\n".format(self.tag))

    def render_kwargs(self, out_file):
        out_file.write("<{}".format(self.tag))
        for kwarg, value in self.kwargs.items():
            if kwarg == 'clas':
                out_file.write(" class='{}'".format(value))
            else:
                out_file.write(" {}='{}'".format(kwarg, value))

    def render_content(self, out_file):
        for content in self.contents:
            try:
                content.render(out_file)
            except AttributeError:
                out_file.write(content)


class Html(Element):
    tag = 'html'


class Body(Element):
    tag = 'body'


class P(Element):
    tag = 'p'


class Head(Element):
    tag = 'head'


class OneLineTag(Element):
    def render(self, out_file):
        if self.kwargs:
            self.render_kwargs(out_file)
            out_file.write("> ")
        else:
            out_file.write("<{}> ".format(self.tag))

        self.render_content(out_file)
        out_file.write(" </{}>\n".format(self.tag))


class Title(OneLineTag):
    tag = 'title'


class SelfClosingTag(Element):
    def render(self, out_file):
        if self.kwargs:
            self.render_kwargs(out_file)
            out_file.write(" />\n")
        else:
            out_file.write("<{} />\n".format(self.tag))

        self.render_content(out_file)


class Hr(SelfClosingTag):
    tag = 'hr'


class Br(SelfClosingTag):
    tag = 'br'


class A(Element):
    tag = 'a'

    def __init__(self, link, contents=None, **kwargs):
        """ 
        I'm a little confused about where to call 'Element.__init__'.
        I can't pass 'contents' to it without getting:
            AttributeError: 'str' object has no attribute 'contents'
        haven't figured out why yet but it works the way it is.
        """
        Element.__init__(self)
        self.link = link
        if contents:
            self.contents = [contents]
        else:
            self.contents = []
        self.kwargs = kwargs

    def render(self, out_file):
        if self.kwargs:
            self.render_kwargs(out_file)
            out_file.write("href='{}'".format(self.link))
            out_file.write(">")
        else:
            out_file.write("<{} href='{}'>".format(self.tag, self.link))

        self.render_content(out_file)
        out_file.write("</{}>\n".format(self.tag))