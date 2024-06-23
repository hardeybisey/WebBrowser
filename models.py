class Base:
    "A tag node in the HTML tree."
    def __init__(self, tag:str, attributes:dict, parent:object=None) -> None:
        self.tag:str = tag
        self.attributes = attributes
        self.parent = parent
        self.children = []
        self.text = ""

    def __repr__(self):
        return f"<{self.tag}>"
    
class Tag(Base):
    "An Opening tag node in the HTML tree."
class SelfClosingTag(Base):
    "A self closing tag node in the HTML tree."
class ClosingTag(Base):
    "A closing tag node in the HTML tree"
    def __repr__(self):
        return f"<{self.tag}>"
class Text:
    "A text node in the HTML tree."
    def __init__(self, text: str) -> None:
        self.text = text
        self.children = []
        
    def __repr__(self):
        return f"{self.text}"