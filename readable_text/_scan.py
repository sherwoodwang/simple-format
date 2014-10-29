from ._parse import parse
import re

class AttibutedLine:
    __ptn_space = re.compile('^ *')

    def __init__(self, data):
        self.data = data

    def lspaces(self):
        m = self.__ptn_space.match(self.data)
        return m.span()[1]

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
            line.content_start = sp
        alines.append(line)

    return alines

def scan2(alines):
    """Adjust indents for ordered lists"""

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
                if alines[i].type == 'ordered' and alines[i].outer_indent == self.outer_indent:
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
            while active_levels and active_levels[-1].outer_indent > aline.content_start:
                active_levels.pop().setup(i)

    while active_levels:
        active_levels.pop().setup(i)
    return alines

def scan3(alines):
    """deal with indents in text lines"""

    outer_indent = [0]
    for i in range(len(alines)):
        aline = alines[i]
        if aline.type in ['ordered', 'unordered']:
            while outer_indent[-1] >= aline.outer_indent:
                outer_indent.pop()
            outer_indent.append(aline.outer_indent)
        elif aline.type == 'text':
            while outer_indent[-1] > aline.content_start:
                outer_indent.pop()
            aline.indent = outer_indent[-1]
    return alines

def scan4(alines):
    """mark explicitly paragraphical list items"""

    explicitly_paragraphical = True
    for aline in alines:
        if aline.type == 'empty':
            explicitly_paragraphical = True
        else:
            if aline.type in ['ordered', 'unordered']:
                aline.explicitly_paragraphical = explicitly_paragraphical

            explicitly_paragraphical = False

    return alines

def scan5(alines, text_parser):
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
                    self.explicitly_paragraphical = aline.explicitly_paragraphical
                    self._child = MultiParagraphContext(self.outer_indent)
                    self._child.append(aline, no_check = True)
                    self._first_line = False
                    return True
                else:
                    if aline.type == 'empty':
                        assert False
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
                elems = [e for d in self.data for e in d.result()]

                paragraphical = self.explicitly_paragraphical
                import sys
                if not paragraphical:
                    num_of_par = 0
                    for elem in elems:
                        if elem[0] == 'paragraph':
                            num_of_par += 1
                    if num_of_par > 1:
                        paragraphical = True

                if not paragraphical:
                    new_elems = []
                    for elem in elems:
                        if elem[0] == 'paragraph':
                            new_elems.extend(elem[1])
                        else:
                            new_elems.append(elem)
                    elems = new_elems

                return elems

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
            self.lines = []
            self.indent = indent

        def append(self, aline, no_check = False):
            if aline is None:
                return False

            if aline.type == 'empty' or \
                    (aline.type == 'text' and aline.indent == self.indent or \
                    no_check):
                self.lines.append(aline)
                return True
            else:
                return False

        def result(self):
            min_start = min((line.content_start for line in self.lines))

            data = []
            constructing = None

            def reduce():
                nonlocal data, constructing

                if constructing:
                    data.append(constructing)
                constructing = None

            for line in self.lines:
                text = line.data[line.content_start:] 
                if text == '':
                    reduce()
                else:
                    if text.startswith('>'):
                        if not isinstance(constructing, QuoteBlock):
                            reduce()
                            constructing = QuoteBlock()
                    else:
                        if not isinstance(constructing, ParagraphBlock):
                            reduce()
                            constructing = ParagraphBlock()
                    constructing.add(text)
            reduce()

            return [e for d in data for e in d.result()]

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
                    return [('rule', )]

                m = ParagraphBlock.__ptn_title.match(self.lines[0])
                if m:
                    return [('title', m.span(1)[1], text_parser(self.lines[0][m.span()[1]:]))]
            elif len(self.lines) == 2:
                m = ParagraphBlock.__ptn_srule.match(self.lines[1])
                if m:
                    return [('title', 2, text_parser(self.lines[0]))]
                m = ParagraphBlock.__ptn_drule.match(self.lines[1])
                if m:
                    return [('title', 1, text_parser(self.lines[0]))]

            text = ''
            for line in self.lines:
                if ParagraphBlock.__ptn_imp_space.match(line):
                    text += ' '
                text += line

            return [('paragraph', text_parser(text))]

    class QuoteBlock:
        __ptn = re.compile('>\\s*')

        def __init__(self):
            self.lines = []

        def add(self, line):
            self.lines.append(line)

        def result(self):
            min_spaces = min((QuoteBlock.__ptn.match(line).span()[1] for line in self.lines))
            lines = [line[min_spaces:] for line in self.lines]
            return [('quote', scan(lines))]

    doc = DocumentContext()
    for aline in alines:
        doc.append(aline)
    doc.append(None)
    return doc.result()

def scan(lines, text_parser=parse):
    return scan5(scan4(scan3(scan2(scan1(lines)))), text_parser)
