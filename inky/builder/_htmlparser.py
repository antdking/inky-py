from html.parser import HTMLParser
from ..nodes.constants import TEXT_NODE_NAME


class NodeTreeBuilder(HTMLParser):

    def __init__(self, node_factory):
        self._nodes = []
        self._root_node = None
        self.node_factory = node_factory
        super().__init__(convert_charrefs=False)

    def handle_starttag(self, tag, attrs):
        node = self.node_factory(tag)
        if attrs:
            for attr_name, attr_val in attrs:
                node.add_attribute(attr_name, attr_val)
        try:
            self._nodes[0].add_node(node)
        except IndexError:
            self._root_node = node
        self._nodes.insert(0, node)

    def handle_endtag(self, tag):
        if tag != self._nodes[0].name:
            raise ValueError("mismatched tag: %s: %s" % (tag, self.getpos()))
        self._nodes.pop(0)

    def handle_startendtag(self, tag, attrs):
        node = self.node_factory(tag, self_closing=True)
        if attrs:
            for attr_name, attr_val in attrs:
                node.add_attribute(attr_name, attr_val)
        self._nodes[0].add_node(node)

    def handle_data(self, data):
        node = self.node_factory(TEXT_NODE_NAME)
        node.add_text(data)
        try:
            self._nodes[0].add_node(node)
        except IndexError:
            pass

    @property
    def node_tree(self):
        return self._root_node


from . import tree_builder_factory
tree_builder_factory.register('htmlparser', NodeTreeBuilder)
