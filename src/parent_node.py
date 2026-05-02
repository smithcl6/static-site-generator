from htmlnode import HTMLNode
import functools

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list[HTMLNode], props:dict[any] = None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode has no tag object.")
        if not self.children:
            raise ValueError("ParentNode has no children.")
        return f'<{self.tag}{self.props_to_html() if self.props else ""}>{str(functools.reduce(lambda accumulator, child: accumulator + child.to_html(), self.children, ""))}</{self.tag}>'
    
