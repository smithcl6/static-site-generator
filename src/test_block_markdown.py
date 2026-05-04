import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_line(self):
        md = """
This is all.
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, ["This is all."])

    def test_markdown_to_blocks_excessive_blanks(self):
        pass
        md = """
Look at me. I originally had five trailing spaces.     






This is a silly use of space.
"""
        blocks = markdown_to_blocks(md)
        expected_list:list[str] = [
            "Look at me. I originally had five trailing spaces.",
            "This is a silly use of space."
        ]
        self.assertListEqual(blocks, expected_list)

    def test_markdown_to_blocks_empty(self):
        self.assertListEqual(markdown_to_blocks(""), [])

    def test_block_to_block_type_standard(self):
        blocks:list[str] = [
            "## This is a heading",
            '```\nprint("hello world")\n```',
            "> This is a quote\n>that spans multiple lines",
            "- item one\n- item two\n- item three",
            "1. first item\n2. second item\n3. third item",
            "This is just normal text."
        ]
        expected_types:list[BlockType] = [
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH
        ]
        self.assertListEqual(list(map(block_to_block_type, blocks)), expected_types)

    def test_block_to_block_type_headings(self):
        blocks:list[str] = [
            "# h1",
            "## h2",
            "### h3",
            "#### h4",
            "##### h5",
            "###### h6",
            "####### h7...?",
            "#broken",
            "# #actually h1",
            " # broken",
        ]
        expected_types:list[BlockType] =[
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
        ]
        self.assertListEqual(list(map(block_to_block_type, blocks)), expected_types)

    def test_block_to_block_type_ordered_list(self):
        blocks:list[str] = [
            "1. Valid\n2. List",
            "2. Not\n3. Valid",
            "2. Also\n1. Invalid",
            "1.Again invalid",
            "1. But this is okay."
        ]
        expected_types:list[BlockType] = [
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.ORDERED_LIST,
        ]
        self.assertListEqual(list(map(block_to_block_type, blocks)), expected_types)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )