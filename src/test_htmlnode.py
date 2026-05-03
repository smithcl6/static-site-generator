from __future__ import annotations
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_string(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
        }
        props_as_string = ' href="https://www.boot.dev" target="_blank"'
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
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_dif_tags(self):
        node = LeafNode("p", "Yo")
        node2 = LeafNode("div", "Yo")
        self.assertNotEqual(node.to_html(), node2.to_html())

    def test_leaf_to_html_with_props(self):
        props = {"style": "color: blue;"}
        node = LeafNode("p", "The Fitness Gram Pacer Test is a...", props)
        self.assertEqual(node.to_html(), '<p style="color: blue;">The Fitness Gram Pacer Test is a...</p>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_grandchildren(self):
        children_nodes = [
            LeafNode("span", "child1", {"style": "background-color: purple"}),
            LeafNode("div", "child2"),
            ParentNode("section", [LeafNode("p", "I am extra nested!")])
        ]
        parent_node = ParentNode("div", children_nodes, {"class": "p-4 m-2"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="p-4 m-2"><span style="background-color: purple">child1</span><div>child2</div><section><p>I am extra nested!</p></section></div>'
        )

    def test_to_html_very_nested(self):
        leaf = LeafNode("p", "hi")
        level5 = ParentNode("div",[leaf])
        level4 = ParentNode("div", [level5])
        level3 = ParentNode("div", [level4])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("div", [level2])
        parent = ParentNode("div", [level1])
        self.assertEqual(parent.to_html(), "<div><div><div><div><div><div><p>hi</p></div></div></div></div></div></div>")
