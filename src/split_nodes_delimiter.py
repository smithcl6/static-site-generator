from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            # if delimiter count of node text is odd, raise exception
            if node.text.count(delimiter) % 2 != 0:
                raise Exception(f"Invalid count of delimiter: {delimiter} in {node.text}")
            split_node:list[str] = node.text.split(delimiter)
            sub_nodes:list[TextNode] = []
            for i in range(0, len(split_node)):
                if i % 2 == 0:
                    sub_nodes.append(TextNode(split_node[i], TextType.TEXT))
                else:
                    sub_nodes.append(TextNode(split_node[i], text_type))
            new_nodes.extend(sub_nodes)

    return new_nodes