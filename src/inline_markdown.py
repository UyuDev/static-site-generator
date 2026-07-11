from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    valid_delimiter = ["**", "_", "`"]
    if delimiter not in valid_delimiter:
        raise Exception("invalid Markdown delimiter")
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("invalid Markdown syntax - missing closing delimiter")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                elif i % 2 == 0:
                    new_node = TextNode(split_text[i], TextType.TEXT)
                    final_list.append(new_node)
                else:
                    new_node = TextNode(split_text[i], text_type)
                    final_list.append(new_node)
    return final_list





