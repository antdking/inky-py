from .base import AbstractNode


class TextNode(AbstractNode):
    __slots__ = ('text', 'name')

    def __init__(self, name):
        self.name = name
        self.text = ''

    def add_text(self, text):
    	self.text += text

    def render(self, modifiers=None):
        return self.text


def text_node_factory(tag_name, self_closing=False):
    return TextNode(tag_name)
