class HTMLNode:
    def __init__(self, tag=None, value=None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        if self.props is not None:
            for keys, value in self.props.items():
                result += f"{keys}=\"{value}\" "
        return result.rstrip()
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag},value={self.value},children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self,tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag is None:
            return self.value
        props = ""
        if self.props is not None:
            props = " " + self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag for a ParentNode, must have one")
        if self.children is None:
            raise ValueError("no children for a ParentNode, must have some")
        props = ""
        if self.props is not None:
            props = " " + self.props_to_html()
        value = ""
        for child in self.children:
            value += child.to_html()
        return f"<{self.tag}{props}>{value}</{self.tag}>"