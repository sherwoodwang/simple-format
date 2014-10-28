from ._parse import parse
import re

class AttibutedLine:
    __ptn_space = re.compile('^ *')

    def __init__(self, data):
        self.data = data

    def lspaces(self):
        m = self.__ptn_space.match(self.data)
        return m.span()[1]

    def content(self):
        if self.type == 'empty':
            return ''
        elif self.type in ['ordered', 'unordered']:
            return self.data[self.content_start:]
        else:
            return self.data[self.indent:]

def scan1(lines):
    """Attribute each line with their format info"""
    _ptn_list = re.compile('(?P<oind>(?P<iind> +)(?:\\d+\\.|\\*)) +')

    def lspaces(self):
        m = self._ptn_space.match(self.line)
        return m.span()[1]

    alines = []
    for rline in lines:
        m = _ptn_list.match(rline)
        line = AttibutedLine(rline)
        if m:
            if m.group('oind')[-1] == '.':
                line.type = 'ordered'
                line.inner_indent = m.span('iind')[1]
                line.outer_indent = m.span('oind')[1]
                line.content_start = m.span()[1]
            else:
                line.type = 'unordered'
                line.inner_indent = m.span('iind')[1]
                line.outer_indent = m.span('oind')[1]
                line.indent = line.inner_indent
                line.content_start = m.span()[1]
        else:
            line.type = 'text'
            sp = line.lspaces()
            if sp == len(line.data):
                line.type = 'empty'
            line.spaces = sp
        alines.append(line)

    return alines

def scan2(alines):
    """Adjust indent for ordered lists"""
    class Level:
        def __init__(self, nl, inner_indent, outer_indent):
            self.nl = nl
            self.inner_indent = inner_indent
            self.outer_indent = outer_indent
            self.indent = inner_indent

        def update_indent(self, indent):
            if self.indent > indent:
                self.indent = indent

        def setup(self, to):
            for i in range(self.nl, to):
                if alines[i].type == 'ordered':
                    alines[i].indent = self.indent

    active_levels = []

    for i in range(len(alines)):
        aline = alines[i]
        if aline.type == 'ordered':
            while active_levels and active_levels[-1].outer_indent > aline.outer_indent:
                active_levels.pop().setup(i)
            if active_levels:
                if active_levels[-1].outer_indent < aline.outer_indent:
                    active_levels.append(Level(i, aline.outer_indent, aline.outer_indent))
                elif active_levels[-1].outer_indent == aline.outer_indent:
                    active_levels[-1].update_indent(aline.inner_indent)
            else:
                active_levels.append(Level(i, aline.outer_indent, aline.outer_indent))
        elif aline.type == 'unordered':
            while active_levels and active_levels[-1].outer_indent > aline.indent:
                active_levels.pop().setup(i)
        elif aline.type == 'text':
            while active_levels and active_levels[-1].outer_indent > aline.spaces:
                active_levels.pop().setup(i)

    while active_levels:
        active_levels.pop().setup(i)
    return alines

def scan3(alines):
    """deal with indent in text lines"""

    outer_indent = [0]
    for i in range(len(alines)):
        aline = alines[i]
        if aline.type in ['ordered', 'unordered']:
            while outer_indent[-1] >= aline.outer_indent:
                outer_indent.pop()
            outer_indent.append(aline.outer_indent)
        elif aline.type == 'text':
            while outer_indent[-1] > aline.spaces:
                outer_indent.pop()
            aline.indent = outer_indent[-1]
    return alines

class DocumentObjectContext:
    def __init__(self):
        self._child = None

    def append(self, aline):
        while True:
            if self._child:
                if self._child.append(aline):
                    return True
                else:
                    self._add(self._child)
                    self._child = None
            else:
                if aline is None:
                    return False

                ret = self._feed(aline)
                if ret is True or ret is False:
                    return ret

    def _add(self, elem):
        raise NotImplementedError()

    def _feed(self, aline):
        raise NotImplementedError()

class DocumentContext(DocumentObjectContext):
    def __init__(self):
        super().__init__()
        self._child = None
        self.data = []

    def _add(self, elem):
        self.data.append(elem)

    def _feed(self, aline):
        if aline.type == 'ordered' or aline.type == 'unordered':
            self._child = ListContext(aline.type, aline.indent)
        else:
            self._child = MultiParagraphContext()

    def result(self):
        return [('doc', [e for d in self.data for e in d.result()])]

class ListContext(DocumentObjectContext):
    class ListItem(DocumentObjectContext):
        def __init__(self):
            super().__init__()
            self.data = []
            self._first_line = True

        def _add(self, elem):
            self.data.append(elem)

        def _feed(self, aline):
            if self._first_line:
                self.indent = aline.indent
                self.outer_indent = aline.outer_indent
                self._child = MultiParagraphContext(self.outer_indent)
                self._child.add(aline.content())
                self._first_line = False
                return True
            else:
                if aline.type == 'empty':
                    self._child = MultiParagraphContext(self.outer_indent)
                else:
                    if self.indent > aline.indent:
                        return False
                    elif self.indent < aline.indent:
                        if aline.type == 'text':
                            if aline.indent < self.outer_indent:
                                return False
                            self._child = MultiParagraphContext(self.outer_indent)
                        else:
                            self._child = ListContext(aline.type, aline.indent)
                    else:
                        return False
        def result(self):
            return [e for d in self.data for e in d.result()]

    def __init__(self, type, indent):
        super().__init__()
        assert type in ['ordered', 'unordered']
        self.type = type
        self.indent = indent
        self.items = []
        self._child = ListContext.ListItem()

    def _add(self, elem):
        self.items.append(elem)

    def _feed(self, aline):
        if aline.indent < self.indent:
            return False
        elif aline.indent > self.indent:
            self._child = ListContext.ListItem()
            return True
        else:
            if aline.type != self.type:
                return False
            else:
                self._child = ListContext.ListItem()

    def result(self):
        return [(self.type, [e.result() for e in self.items])]

class MultiParagraphContext:
    def __init__(self, indent=0):
        super().__init__()
        self.data = []
        self.indent = indent
        self.__constructing = None

    def add(self, text):
        if text == '':
            self.__reduce()
        else:
            if text.startswith('>'):
                if not isinstance(self.__constructing, QuoteBlock):
                    self.__reduce()
                    self.__constructing = QuoteBlock()
            else:
                if not isinstance(self.__constructing, ParagraphBlock):
                    self.__reduce()
                    self.__constructing = ParagraphBlock()
            self.__constructing.add(text)

    def __reduce(self):
        if self.__constructing:
            self.data.append(self.__constructing)
        self.__constructing = None

    def append(self, aline):
        if aline is None:
            return False

        if aline.type == 'empty' or \
                (aline.type == 'text' and aline.indent == self.indent):
            self.add(aline.content())
            return True
        else:
            return False

    def result(self):
        self.__reduce()
        return [e for d in self.data for e in d.result()]

class ParagraphBlock:
    __ptn_imp_space = re.compile('^.*[0-9a-zA-Z]$')
    __ptn_srule = re.compile('^-{4,}$')
    __ptn_drule = re.compile('^={4,}$')
    __ptn_title = re.compile('^(#{1,6}) +')

    def __init__(self):
        self.lines = []

    def add(self, line):
        self.lines.append(line)

    def result(self):
        if len(self.lines) == 1:
            m = ParagraphBlock.__ptn_srule.match(self.lines[0])
            if m:
                return [('rule')]

            m = ParagraphBlock.__ptn_title.match(self.lines[0])
            if m:
                return [('title', m.span(1)[1], parse(self.lines[0][m.span()[1]:]))]
        elif len(self.lines) == 2:
            m = ParagraphBlock.__ptn_srule.match(self.lines[1])
            if m:
                return [('title', 2, parse(self.lines[0]))]
            m = ParagraphBlock.__ptn_drule.match(self.lines[1])
            if m:
                return [('title', 1, parse(self.lines[0]))]

        text = ''
        for line in self.lines:
            if ParagraphBlock.__ptn_imp_space.match(line):
                text += ' '
            text += line

        return [('paragraph', parse(text))]

class QuoteBlock:
    __ptn = re.compile('>\\s*')

    def __init__(self):
        self.lines = []

    def add(self, line):
        m = QuoteBlock.__ptn.match(line)
        self.lines.append(line[m.span()[1]:])

    def result(self):
        return [('quote', scan(self.lines))]

def scan4(alines):
    doc = DocumentContext()
    for aline in alines:
        doc.append(aline)
    doc.append(None)
    return doc.result()

def scan(lines):
    return scan4(scan3(scan2(scan1(lines))))

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

    def render_doc(self, data):
        for elem in data:
            self.render(elem)

    def render_ordered(self, data):
        self.file.write('<ol>')
        for item in data:
            self.file.write('<li>')
            for elem in item:
                self.render(elem)
            self.file.write('</li>')
        self.file.write('</ol>')

    def render_unordered(self, data):
        self.file.write('<ul>')
        for item in data:
            self.file.write('<li>')
            for elem in item:
                self.render(elem)
            self.file.write('</li>')
        self.file.write('</ul>')

    def render_quote(self, data):
        self.file.write('<quoteblock>')
        for elem in data:
            self.render(elem)
        self.file.write('</quoteblock>')

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
        self.file.write('<h{}>'.format(level))
        for elem in data:
            self.render(elem)
        self.file.write('</h{}>'.format(level))

def render(text, file):
    renderer = HTMLRenderer(file)
    data = scan(text.splitlines())
    renderer(data)
