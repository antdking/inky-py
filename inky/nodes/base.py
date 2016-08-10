class AbstractNode:
    def add_attribute(self, attribute, value):
        return

    def add_class(self, klass):
        return

    def add_node(self, node):
        return

    @property
    def formatted_attributes(self):
        return ''

    @staticmethod
    def format_attributes(attributes):
        if attributes:
            return ' '.join(
                key + '="' + val + '"'
                for key, val in attributes.items()
            )
        return ''

    @property
    def formatted_classes(self):
        return ''

    @staticmethod
    def format_classes(classes):
        if classes:
            return self.format_attributes({'class': ' '.join(classes)})
        return ''

    @property
    def nodes(self):
        return []
    @nodes.setter
    def nodes(self, val):
        return

    def pre_render(self):
        return

    def render(self):
        return ''

    def add_text(self, text):
        raise TypeError("Node does not support taking text directly")
