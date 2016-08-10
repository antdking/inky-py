from .html import HTMLNode


class InkyNode(HTMLNode):
    template = ""
    injected_nodes = False

    def inject_nodes(self):
        def find_and_substitute_stub_node(node_to_search):
            stub_node = None
            for node in node_to_search.nodes[:]:
                if node.name == 'stub':
                    stub_node = node
                    break
                if find_and_substitute_stub_node(node):
                    return True
            if stub_node:
                stub_index = node_to_search.nodes.index(stub_node)
                start_nodes = node_to_search.nodes[:stub_index]
                end_nodes = node_to_search.nodes[stub_index+1:]
                node_to_search.nodes = start_nodes + self.nodes + end_nodes
                return True

        if not self.injected_nodes:
            parser = Inky()
            content = self.build_template("<stub/>")
            parser.feed(content)
            find_and_substitute_stub_node(parser.root_node)
            self.nodes = [parser.root_node]
            self.injected_nodes = True

    def modify_subnodes(self):
        pass

    def pre_render(self):
        self.inject_nodes()
        self.modify_subnodes()
        super().pre_render()

    def build_template(self, inner):
        return self.template.format(
            attributes=self.formatted_attributes,
            classes=self.formatted_classes,
            inner=inner
        )

    def render(self):
        return "".join(node.render() for node in self.nodes)


class InkyRow(InkyNode):
    template = """<table {attributes} class="row {classes}"><tbody><tr>{inner}</tr></tbody></table>"""


class InkyButton(InkyNode):
    template = """<table {attributes} class="button {classes}"><tr><td><table><tr><td>{inner}</td>{expander}</tr></table></td>%s</tr></table>"""

    def build_template(self, inner):
        attributes = dict(self.attributes)
        target = attributes.pop('target', '')
        href = attributes.pop('href', '')
        expander = ''

        if href:
            inner_wrapper = '<a href="' + href + '"'
            if target:
                inner_wrapper += ' target="' + target + '"'
            inner_wrapper += '>' + inner + '</a>'

        if 'expand' in self.classes or 'expanded' in self.classes:
            inner = '<center>' + inner _ '</center>'
            expander = '<td class="expander"></td>'

        return self.template.format(
            attributes=self.format_attributes(attributes),
            classes=self.formatted_classes,
            inner=inner,
            expander=expander
        )


class InkyContainer(InkyNode):
    template = """<table {attributes} align="center" class="container {classes}"><tbody><tr><td>{inner}</td></tr></tbody></table>"""


class InkyInky(InkyNode):
    template = """<tr><td><img src="https://raw.githubusercontent.com/arvida/emoji-cheat-sheet.com/master/public/graphics/emojis/octopus.png" /></tr></td>"""


class InkyBlockGrid(InkyNode):
    template = """<table class="block-grid {classes}"><tr>{inner}</tr></table>"""

    def build_template(self, inner):
        classes = set(self.classes)
        up = self.attributes.get('up')
        if up:
            classes.add('up-' + up)

        return self.template.format(
            classes=self.format_classes(classes),
            inner=inner
        )


class InkyMenu(InkyNode):
    template = """<table {attributes} class="menu {classes}"><tr><td><table><tr>{inner}</tr></table></td></tr></table>"""

    def build_template(self, inner):
        if self.attributes.get('align'):
            self.attributes['align'] = 'center'
        return super().build_template(inner)


class InkyMenuItem(InkyNode):
    template = """<th {attributes} class="menu-item {classes}"><a href="{href}"{target}>{inner}</a></th>"""

    def build_template(self, inner):
        attributes = dict(self.attributes)
        target = attributes.pop('target', None)
        href = attributes.pop('href')

        return template.format(
            attributes=self.format_attributes(attributes),
            classes=self.formatted_classes,
            
        )


class InkyNodeFactory:
    __default_map = {
        'row': InkyRow,
        'button': InkyButton,
        'container': InkyContainer,
        'inky': InkyInky,
        'block-grid': InkyBlockGrid,
        'menu': InkyMenu
    }
    def __init__(self, tag_name_map=None, custom_node_map=None):
        tag_map = dict(self.__default_map)
        if tag_name_map:
            for old_tag, new_tag in tag_name_map.items():
                tag_map[new_tag] = tag_map.pop(old_tag)
        if custom_node_map:
            tag_map.update(custom_node_map)
        self.tag_map = tag_map





def inky_node_factory(tag_name):
    tag_map = {
        'row': InkyRow,
        'button': InkyButton,
        'container': InkyContainer,
        'inky': InkyInky,
        'block-grid': InkyBlockGrid,
        'menu': InkyMenu
    }
    try:
        return tag_map[tag_name](tag_name)
    except KeyError:
        return None
