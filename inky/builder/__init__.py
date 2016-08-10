from . import _htmlparser  # noqa


class TreeBuilderDoesNotExist(Exception):
    pass


class __TreeBuilderFactory:
    __default = 'htmlparser'
    def __init__(self):
        self.__tree_builders = dict()

    def load_core_tree_builders():
        from . import _htmlparser  # noqa

    def register(self, name, builder):
        self.__tree_builders[name] = builder

    def select(name=None):
        if name is None:
            name = self.__default
        try:
            return __TREE_BUILDERS[name]
        except KeyError:
            raise TreeBuilderDoesNotExist() from None

tree_builder_factory = __TreeBuilderFactory()
tree_builder_factory.load_core_tree_builders()