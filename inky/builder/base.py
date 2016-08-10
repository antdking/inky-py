class AbstractNodeTreeBuilder:
    def __init__(self, node_factory):
        self.node_factory = node_factory

    @property
    def node_tree(self):
        raise NotImplementedError
