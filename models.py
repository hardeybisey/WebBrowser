class Tag:
    "A tag node in the HTML tree."
    def __init__(self, tag:str, attributes:dict, prev:object=None) -> None:
        self.tag:str = tag
        self.attributes = attributes
        self.prev = prev
        self.next = None
        self.text = ""

    def __repr__(self):
        return f"<{self.tag}>"

class ClosingTag:
    "A closing tag node in the HTML tree"
    def __init__(self, tag:str, attributes:dict, prev:object=None) -> None:
        self.tag:str = tag
        self.attributes = attributes
        self.prev = prev
        self.next = None
        self.text = ""
        
    def __repr__(self):
        return f"<{self.tag}>"

class SelfClosingTag:
    "A self closing tag node in the HTML tree."
    def __init__(self, tag:str, attributes:dict, prev:object=None) -> None:
        self.tag:str = tag
        self.attributes = attributes
        self.prev = prev
        self.next = None
        self.text = ""
        
    def __repr__(self): 
        return f"<{self.tag} />"

class Text:
    "A text node in the HTML tree."
    def __init__(self, text: str) -> None:
        self.text = text
        
    def __repr__(self):
        return f"{self.text}"