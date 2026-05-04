import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

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