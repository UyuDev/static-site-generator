

class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        formatted_string = ""
        for key in self.props:
            formatted_string += f' {key}="{self.props[key]}"'
        return formatted_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super().__init__(tag, value, props=props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        # for links and images the spacing is different so I separated them
        if self.tag == 'a':
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        elif self.tag == 'img':
            return f'<{self.tag}{self.props_to_html()} />'
        elif self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
       

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("missing tag value")
        if self.children is None:
            raise ValueError("missing children value")
        formatted_string = f"<{self.tag}>"
        for child in self.children:
            formatted_string += child.to_html()
        return formatted_string + f"</{self.tag}>"