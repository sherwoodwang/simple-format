from ._scan import scan

class Renderer:
    def render(self, data):
        def call_renderer(name, *args):
            getattr(self, 'render_' + name)(*args)
        return call_renderer(*data)

    def __call__(self, data):
        assert isinstance(data, list) and len(data) == 1
        return self.render(data[0])

import html
class HTMLRenderer(Renderer):
    def __init__(self, file):
        super().__init__()
        self.file = file
        self.render_paragraph = self.__render_paragraph_exp

    def render_doc(self, data):
        for elem in data:
            self.render(elem)

    def __render_li(self, item):
        self.file.write('<li>')
        num_of_non_list = 0
        for elem in item:
            if elem[0] not in ['ordered', 'unordered']:
                num_of_non_list += 1
        if num_of_non_list <= 1:
            original = self.render_paragraph
            self.render_paragraph = self.__render_paragraph_imp
            for elem in item:
                self.render(elem)
            self.render_paragraph = original
        else:
            for elem in item:
                self.render(elem)
        self.file.write('</li>')

    def render_ordered(self, data):
        self.file.write('<ol>')
        for item in data:
            self.__render_li(item)
        self.file.write('</ol>')

    def render_unordered(self, data):
        self.file.write('<ul>')
        for item in data:
            self.__render_li(item)
        self.file.write('</ul>')

    def render_quote(self, data):
        self.file.write('<blockquote>')
        for elem in data:
            self.render(elem)
        self.file.write('</blockquote>')

    def __render_paragraph_exp(self, data, implicit_paragraph=False):
        self.file.write('<p>')
        for elem in data:
            self.render(elem)
        self.file.write('</p>')

    def __render_paragraph_imp(self, data, implicit_paragraph=False):
        for elem in data:
            original = self.render_paragraph
            self.render_paragraph = self.__render_paragraph_exp
            self.render(elem)
            self.render_paragraph = original

    def render_text(self, data):
        self.file.write(html.escape(data))

    def render_strong(self, data):
        self.file.write('<strong>')
        for elem in data:
            self.render(elem)
        self.file.write('</strong>')

    def render_em(self, data):
        self.file.write('<em>')
        for elem in data:
            self.render(elem)
        self.file.write('</em>')

    def render_title(self, level, data):
        self.file.write('<h{}>'.format(level))
        for elem in data:
            self.render(elem)
        self.file.write('</h{}>'.format(level))

    def render_rule(self):
        self.file.write('<hr>')

def render_as_html(text, file):
    renderer = HTMLRenderer(file)
    data = scan(text.splitlines())
    renderer(data)
