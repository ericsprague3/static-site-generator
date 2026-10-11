class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented

    def props_to_html(self) -> str:
        if self.props is not None:
            prop_line = ""
            for key, value in self.props.items():
                prop_line += f" {key}={value}"
            return prop_line
        else:
            return ""

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode missing value")
        if self.tag is None:
            return self.value

        props = super().props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return NotImplemented
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode missing tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode missing children")

        child_html = ""
        for child in self.children:
            child_html += child.to_html()

        return f"<{self.tag}>{child_html}</{self.tag}>"

    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return NotImplemented
        return (
            self.tag == other.tag and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"