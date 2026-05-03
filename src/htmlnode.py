from __future__ import annotations
import functools

class HTMLNode:
    def __init__(self, tag:str=None, value:str=None, children:list[HTMLNode]=None, props:dict[any]=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        return str(functools.reduce(lambda accumulator, dict: accumulator + f' {dict[0]}="{dict[1]}"' , list(self.props.items()), ""))
    
    def __repr__(self):
        return f"HTMLNode({self.tag} {self.value} {self.children} {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag:str, value:str = None, props:dict[any] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All Leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

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
