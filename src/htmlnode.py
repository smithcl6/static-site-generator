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
        
        return str(functools.reduce(lambda accumulator, dict: accumulator + f'{dict[0]}="{dict[1]}" ' , list(self.props.items()), ""))
    
    def __repr__(self):
        print(f"{self.tag} {self.value} {self.children} {self.props}")