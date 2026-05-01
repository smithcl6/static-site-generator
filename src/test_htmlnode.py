from __future__ import annotations
import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_string(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        props_as_string = 'href="https://www.boot.dev" target="_blank" '
        node = HTMLNode("div", "bee movie script", None, props)
        self.assertEqual(props_as_string, node.props_to_html());

    def test_prop_html_matching_nodes(self):
        props1 = {
            "style": "color: red;",
            "onclick": "doFunction()"
        }
        props2 = {
            "style": "color: red;",
            "onclick": "doFunction()"
        }
        node = HTMLNode("button", "Click Me!", None, props1)
        node2 = HTMLNode("button", "Click Me!", None, props2)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_prop_html_same_prop_dif_node(self):
        props ={"href": "https://www.boot.dev"}
        node = HTMLNode("a", "Boot Dev", None, props)
        node2 = HTMLNode("a", "Click this Link", None, props)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_prop_html_None(self):
        node = HTMLNode("div", "lorem ipsum", None, None)
        node2 = HTMLNode("div", "lorem ipsum", None, None)
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        
