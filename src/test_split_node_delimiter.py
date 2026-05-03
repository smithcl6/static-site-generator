import unittest
from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text.", TextType.TEXT)
        new_nodes:list[TextNode] = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_list:list[TextNode] = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_list))
        for i in range(0, len(expected_list)):
            self.assertEqual(new_nodes[i].text, expected_list[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_list[i].text_type)


    
    def test_italic_delimiter(self):
        node = TextNode("This is _italicized_ text.", TextType.TEXT)
        new_nodes:list[TextNode] = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_list:list[TextNode] = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_list))
        for i in range(0, len(expected_list)):
            self.assertEqual(new_nodes[i].text, expected_list[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_list[i].text_type)

    def test_code_delimiter(self):
        node = TextNode("This text has `code` in it.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_list:list[TextNode] = [
            TextNode("This text has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_list))
        for i in range(0, len(expected_list)):
            self.assertEqual(new_nodes[i].text, expected_list[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_list[i].text_type)

    def test_multiple_input_nodes(self):
        node = TextNode("I have some **bold** text.", TextType.TEXT)
        node2 = TextNode("I do **too!**", TextType.TEXT)
        new_nodes:list[TextNode] = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        expected_list:list[TextNode] = [
            TextNode("I have some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("I do ", TextType.TEXT),
            TextNode("too!", TextType.BOLD),
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_list))
        for i in range(0, len(expected_list)):
            self.assertEqual(new_nodes[i].text, expected_list[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_list[i].text_type)


    def test_multiple_type_instances(self):
        node = TextNode("_I_ should be _italicized_.", TextType.TEXT)
        node2 = TextNode("_I too_ am _italicized_. Hopefully that is okay.", TextType.TEXT)
        new_nodes:list[TextNode] = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        expected_list:list[TextNode] = [
            TextNode("", TextType.TEXT),
            TextNode("I", TextType.ITALIC),
            TextNode(" should be ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
            TextNode("", TextType.TEXT),
            TextNode("I too", TextType.ITALIC),
            TextNode(" am ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(". Hopefully that is okay.", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_list))
        for i in range(0, len(expected_list)):
            self.assertEqual(new_nodes[i].text, expected_list[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_list[i].text_type)

    def test_delimiter_with_varying_input_types(self):
        input_nodes:list[TextNode] = [
            TextNode("I should be completely bold already.", TextType.BOLD),
            TextNode("I should be normal text", TextType.TEXT),
            TextNode("I have bold as **part** of my text.", TextType.TEXT),
            TextNode("_My italicized_ and `code types` should be ignored here", TextType.TEXT)
        ]
        new_nodes:list[TextNode] = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected_list:list[TextNode] = [
            TextNode("I should be completely bold already.", TextType.BOLD),
            TextNode("I should be normal text", TextType.TEXT),
            TextNode("I have bold as ", TextType.TEXT),
            TextNode("part", TextType.BOLD),
            TextNode(" of my text.", TextType.TEXT),
            TextNode("_My italicized_ and `code types` should be ignored here", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_list))
        for i in range(0, len(expected_list)):
            self.assertEqual(new_nodes[i].text, expected_list[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_list[i].text_type)
    
    def test_subsequent_delimiters(self):
        node = TextNode("`Hi ``there`. I should be two code types and a text type.", TextType.TEXT)
        new_nodes:list[TextNode] = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_list:list[TextNode] = [
            TextNode("", TextType.TEXT),
            TextNode("Hi ", TextType.CODE),
            TextNode("", TextType.TEXT),
            TextNode("there", TextType.CODE),
            TextNode(". I should be two code types and a text type.", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_list))
        for i in range(0, len(expected_list)):
            self.assertEqual(new_nodes[i].text, expected_list[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_list[i].text_type)



    def test_no_delimiter_found(self):
        node = TextNode("I have no delimiters!", TextType.TEXT)
        new_nodes:list[TextNode] = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "I have no delimiters!")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
