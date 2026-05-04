import unittest
from block_markdown import markdown_to_blocks

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