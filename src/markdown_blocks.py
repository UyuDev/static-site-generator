

def markdown_to_blocks(markdown: str) -> list[str]:
    split_text = markdown.split("\n\n")
    final_list = []
    for text in split_text:
        if text == "":
            continue
        final_list.append(text.strip())
    return final_list
    