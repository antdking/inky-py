from .base import AbstractNode


class HTMLNode(AbstractNode):
    __slots__ = ('name', 'attributes', 'classes', '_nodes')

    def __init__(self, name):
        self.name = name
        self.attributes = dict()
        self.classes = set()
        self._nodes = []

    def add_attribute(self, attribute, value):
        if attribute == 'class':
            for klass in value.split():
                self.add_class(value)
        else:
            self.attributes[attribute] = value

    def add_class(self, klass):
        klass = klass.strip()
        if klass:
            self.classes.add(klass)

    def add_node(self, node):
        self.nodes.append(node)

    @property
    def nodes(self):
        return self._nodes
    @nodes.setter
    def nodes(self, val):
        self._nodes = val

    @property
    def formatted_attributes(self):
        return self.format_attributes(self.attributes)

    @property
    def formatted_classes(self):
        return self.format_classes(self.classes)

    def generate_start_tag(self):
        start_tag = "<" + self.name
        classes = self.formatted_classes
        if classes:
            start_tag += ' ' + classes
        attributes = self.formatted_attributes
        if attributes:
            start_tag += ' ' + attributes
        start_tag += '>'
        return start_tag

    def pre_render(self):
        for node in self.nodes:
            node.pre_render()

    def render(self):
        start_tag = self.generate_start_tag()
        contents = "".join(node.render() for node in self.nodes)
        end_tag = '</' + self.name + '>'
        return start_tag + contents + end_tag



class SelfClosingHTMLNode(HTMLNode):
    def render(self):
        tag = '<' + name
        classes = self.formatted_classes
        if classes:
            tag += ' ' + classes
        attributes = self.formatted_attributes
        if attributes:
            tag += ' ' + attributes
        tag += '/>'
        return tag


def html_node_factory(tag_name, self_closing=False):
    if self_closing:
        return SelfClosingHTMLNode(tag_name)
    return HTMLNode(tag_name)
