from html_parser import Tag

class CSSParser:
    def __init__(self, text):
        self.text = text
        self.index = 0

    def white_space(self):
        # advance the index if the current character is a white space 
        # but dont return it since it is not needed
        while self.index < len(self.text) and self.text[self.index].isspace():
            self.index += 1
            
    def word(self):
        # parse a single word from the text
        start = self.index
        while self.index < len(self.text):
            current = self.text[self.index]
            if current.isalnum() or current in "#-.%":
                self.index += 1
            else:
                break
        if not (self.index > start):
            raise Exception("Word parsing Error")
        return self.text[start:self.index]
    
    def literal(self, value):
        # advance the index if the current character is a literal value (e.g. ":", ";")
        if not (self.index < len(self.text) and self.text[self.index] == value):
            raise Exception(f"Literal parsing Error")
        self.index += 1
        
    def pair(self):
        # parse a single key value pair
        key = self.word()
        self.white_space()
        self.literal(":")
        self.white_space()
        value = self.word()
        return key, value
    
    def body(self):
        # parse the whole attributes as a block of text and store them
        #  as key value pairs
        pairs = {}
        while self.index < len(self.text):
            try:
                key, value = self.pair()
                pairs[key] = value
                self.white_space()
                self.literal(";")
                self.white_space()
            except Exception:
                why = self.ignore_until([";"])
                if why == ";":
                    self.literal(";")
                    self.white_space()
                else:
                    break
        return pairs
    
    def ignore_until(self, chars):
        # function to ignore characters until a certain character is found
        #  used for error handling and making sure all characters are parsed
        while self.index < len(self.text):
            if self.text[self.index] in chars:
                return self.text[self.index]
            else:
                self.index += 1
        return None
    
    # def selector(self):
    #     out = TagSelector(self.word())
    #     self.white_space()
    #     while self.index < len(self.text) and self.text[self.index] != "{":
    #         tag = self.word()
    #         descendant = TagSelector(tag)
    #         out = DescendantSelector(out, descendant)
    #         self.white_space()
    #     return out

    
    
def style(node):
    # recursively parse the a node to get all the style attribute
    # of the node and its children and store it as the node attribute
    node.style = {}
    if isinstance(node, Tag) and "style" in node.attributes:
        pairs = CSSParser(node.attributes["style"]).body()
        for key, value in pairs.items():
            node.style[key] = value
    for child in node.children:
        style(child)
        
        
class TagSelector:
    def __init__(self, tag):
        self.tag = tag
        
    def matches(self, node):
        return isinstance(node, Tag) and node.tag == self.tag

    def __repr__(self) -> str:
        return f"{self.tag}"

class DescendantSelector:
    def __init__(self, ancestor, descendant):
        self.ancestor = ancestor
        self.descendant = descendant
        
    
    def __repr__(self) -> str:
        return f"{self.ancestor} {self.descendant}"
        
    def matches(self, node):
        if not isinstance(node, Tag):
            return False
        if not self.descendant.matches(node): return False
        while node.parent:
            if self.ancestor.matches(node.parent): return True
            node = node.parent
        return False