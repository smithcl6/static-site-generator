import unittest

from leaf_node import LeafNode

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