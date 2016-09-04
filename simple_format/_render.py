from ._scan import scan
import html


class Renderer:
    def render(self, data):
        def call_renderer(name, *args):
            getattr(self, 'render_' + name)(*args)
        return call_renderer(*data)

    def __call__(self, data):
        assert isinstance(data, list) and len(data) == 1
        return self.render(data[0])


class HTMLRenderer(Renderer):
    def __init__(self, file, title_toplevel=0):
        super().__init__()
        self.file = file
        self.title_toplevel = title_toplevel

    def render_doc(self, data):
        for elem in data:
            self.render(elem)

    def __render_list_item(self, item):
        self.file.write('<li>')
        for elem in item:
            self.render(elem)
        self.file.write('</li>')

    def render_ordered(self, data):
        self.file.write('<ol>')
        for item in data:
            self.__render_list_item(item)
        self.file.write('</ol>')

    def render_unordered(self, data):
        self.file.write('<ul>')
        for item in data:
            self.__render_list_item(item)
        self.file.write('</ul>')

    def render_quote(self, data):
        self.file.write('<blockquote>')
        for elem in data:
            self.render(elem)
        self.file.write('</blockquote>')

    def render_paragraph(self, data):
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
        level += self.title_toplevel
        self.file.write('<h{}>'.format(level))
        for elem in data:
            self.render(elem)
        self.file.write('</h{}>'.format(level))

    def render_rule(self):
        self.file.write('<hr>')


def render_as_html(text, file, title_toplevel=0):
    renderer = HTMLRenderer(file, title_toplevel)
    data = scan(text.splitlines())
    renderer(data)
