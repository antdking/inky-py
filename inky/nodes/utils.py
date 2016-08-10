def nodes_by_name(nodes, name):
    for node in nodes:
        if node.name == name:
            yield node


def nodes_by_class(nodes, class_name):
    for node in nodes:
        if class_name in node.classes:
            yield node


def nodes_by_attribute_name(nodes, attribute_name):
    for node in nodes:
        if attribute_name in node.attributes:
            yield node


def nodes_by_attribute(nodes, attribute_name, attribute_value):
    for node in nodes:
        if attribute_value == node.attributes.get(attribute_name):
            yield node


def deep_nodes(nodes):
    for node in nodes:
        yield node
        yield from deep_nodes(self.nodes)
