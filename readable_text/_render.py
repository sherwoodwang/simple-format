from ._scan import scan

class Renderer:
    def render(self, data, **kwargs):
        def call_renderer(name, *args):
            getattr(self, 'render_' + name)(*args, **kwargs)
        return call_renderer(*data)

    def __call__(self, data):
        assert isinstance(data, list) and len(data) == 1
        return self.render(data[0])

import html
class HTMLRenderer(Renderer):
    def __init__(self, file):
        super().__init__()
        self.file = file

    def render_doc(self, data):
        for elem in data:
            self.render(elem)

    def __render_li(self, item):
        self.file.write('<li>')
        if len(item) == 1 and item[0][0] == 'paragraph':
            self.render(item[0], implicit_paragraph=True)
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

    def render_paragraph(self, data, implicit_paragraph=False):
        if implicit_paragraph:
            for elem in data:
                self.render(elem)
        else:
            self.file.write('<p>')
            for elem in data:
                self.render(elem)
            self.file.write('</p>')

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
