import re


class TextObject:

    @classmethod
    def match(cls, text, pos):
        return cls.lookahead.match(text, pos)

    def result(self):
        raise NotImplementedError()


class TextObjectContainer(TextObject):
    delimiting_required = False

    class Pop(Exception):
        pass

    def __init__(self, text, pos=0, endpos=None):
        super().__init__()

        if endpos is None:
            endpos = len(text)

        assert isinstance(text, str)
        self.text = text
        self.elems = []

        start = end = pos

        def push():
            if start != end:
                self.elems.append((start, end))
        try:
            while end < endpos:
                for syntax_ in self.syntax:
                    if syntax_ is None:
                        syntax = self.delimiter
                    else:
                        syntax = syntax_
                    m = syntax.match(text, end)
                    if m:
                        push()
                        if syntax_ is None:
                            _, self.end = m.span()
                            raise TextObjectContainer.Pop()
                        elem = syntax(text, end, endpos)
                        self.elems.append(elem)
                        start = end = elem.end
                        break
                else:
                    end += 1
            push()
            self.end = endpos
        except TextObjectContainer.Pop:
            self.delimited = True
        else:
            self.delimited = False
            self.end = end

    def result(self):
        return [("text", self.text[elem[0]:elem[1]])
                if isinstance(elem, tuple) else
                elem.result()
                for elem in self.elems]


class TextObjectEscape(TextObject):
    lookahead = re.compile('\\\\')

    def __init__(self, text, pos=0, endpos=None):
        self.ch = text[pos + 1]
        self.end = pos + 2

    def result(self):
        return 'text', self.ch


class TextObjectEm(TextObjectContainer):
    lookahead = re.compile('\\*')
    delimiter = re.compile('\\*')

    def __init__(self, text, pos=0, endpos=None):
        super().__init__(text, pos + 1, endpos)

    def result(self):
        return 'em', super().result()


class TextObjectStrong(TextObjectContainer):
    lookahead = re.compile('\\*\\*')
    delimiter = re.compile('\\*\\*')

    def __init__(self, text, pos=0, endpos=None):
        super().__init__(text, pos + 2, endpos)

    def result(self):
        return 'strong', super().result()


class TextObjectNormal(TextObjectContainer):
    pass

TextObjectStrong.syntax = [TextObjectEscape, None, TextObjectEm]
TextObjectEm.syntax = [TextObjectEscape, TextObjectStrong, None]
TextObjectNormal.syntax = [TextObjectEscape, TextObjectStrong, TextObjectEm]


def parse(text, root_class=TextObjectNormal):
    top = root_class(text)
    return top.result()
