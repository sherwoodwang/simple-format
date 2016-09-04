from ._scan import scan
import html


class Renderer:
    def render(self, data):
        def call_renderer(name, *args):
            yield from getattr(self, 'render_' + name)(*args)
        yield from call_renderer(*data)

    def __call__(self, data):
        assert isinstance(data, list) and len(data) == 1
        yield from self.render(data[0])


class HTMLRenderer(Renderer):
    def __init__(self, title_toplevel=0):
        super().__init__()
        self.title_toplevel = title_toplevel

    def render_doc(self, data):
        for elem in data:
            yield from self.render(elem)

    def __render_list_item(self, item):
        yield '<li>'
        for elem in item:
            yield from self.render(elem)
        yield '</li>'

    def render_ordered(self, data):
        yield '<ol>'
        for item in data:
            self.__render_list_item(item)
        yield '</ol>'

    def render_unordered(self, data):
        yield '<ul>'
        for item in data:
            self.__render_list_item(item)
        yield '</ul>'

    def render_quote(self, data):
        yield '<blockquote>'
        for elem in data:
            yield from self.render(elem)
        yield '</blockquote>'

    def render_paragraph(self, data):
        yield '<p>'
        for elem in data:
            yield from self.render(elem)
        yield '</p>'

    def render_text(self, data):
        yield html.escape(data)

    def render_strong(self, data):
        yield '<strong>'
        for elem in data:
            yield from self.render(elem)
        yield '</strong>'

    def render_em(self, data):
        yield '<em>'
        for elem in data:
            yield from self.render(elem)
        yield '</em>'

    def render_title(self, level, data):
        level += self.title_toplevel
        yield '<h{}>'.format(level)
        for elem in data:
            yield from self.render(elem)
        yield '</h{}>'.format(level)

    def render_rule(self):
        yield '<hr>'


def render_as_html(text, title_toplevel=0):
    renderer = HTMLRenderer(title_toplevel)
    data = scan(text.splitlines())
    yield from renderer(data)
