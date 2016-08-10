from html.parser import HTMLParser
import io


def node_factory(tag_name):
    tag_map = {
        'row': InkyRow,
        'button': InkyButton,
        'container': InkyContainer,
        'inky': InkyInky,
        'block-grid': InkyBlockGrid,
        'menu': InkyMenu

    }
    return tag_map.get(tag_name, HTMLNode)(tag_name)


def release_the_kraken(content):
    from .builder import HTMLParserNodeTreeBuilder
    tree_builder = HTMLParserNodeTreeBuilder(node_factory)
    tree_builder.feed(content)
    node_tree = tree_builder.node_tree
    node_tree.pre_render()
    return node_tree.render()


if __name__ == '__main__':
    release_the_kraken("""
        <container>
            <row>
                <column>
                    <inky></inky>
                </column>
            </row>
        </container>
    """)
