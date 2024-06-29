class Tag:
    "A tag node in the HTML tree."
    def __init__(self, tag:str, attributes:dict, parent:object=None) -> None:
        self.tag:str = tag
        self.attributes = attributes
        self.parent = parent
        self.children = []
        self.text = ""
    
class OpenTag(Tag):
    "An Opening or self closing tag node in the HTML tree."
    def __repr__(self):
        return f"<{self.tag}>"

class CloseTag(Tag):
    "A closing tag node in the HTML tree"
    def __repr__(self):
        return f"</{self.tag}>"
class Text:
    "A text node in the HTML tree."
    def __init__(self, text: str, parent) -> None:
        self.text = text
        self.parent = parent
        self.children = []
        
    def __repr__(self):
        return f"{self.text}"