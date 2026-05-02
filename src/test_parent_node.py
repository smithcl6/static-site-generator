import unittest
from parent_node import ParentNode
from leaf_node import LeafNode

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
        