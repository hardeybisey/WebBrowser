from models import Tag

INHERITED_PROPERTIES = {
    "font-size": "16px",
    "font-style": "normal",
    "font-weight": "normal",
    "color": "black",
}

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
        return key.casefold(), value
    
    def body(self):
        # parse the whole attributes as a block of text and store them
        #  as key value pairs
        pairs = {}
        while self.index < len(self.text) and self.text[self.index] != "}":
            try:
                key, value = self.pair()
                pairs[key.casefold()] = value
                self.white_space()
                self.literal(";")
                self.white_space()
            except Exception:
                why = self.ignore_until([";", "}"])
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
    
    def selector(self):
        out = TagSelector(self.word())
        self.white_space()
        while self.index < len(self.text) and self.text[self.index] != "{":
            tag = self.word()
            descendant = TagSelector(tag)
            out = DescendantSelector(out, descendant)
            self.white_space()
        return out
    
    def parse(self):
        rules = []
        while self.index < len(self.text):
            try:
                self.white_space()
                selector = self.selector()
                self.literal("{")
                self.white_space()
                body = self.body()
                self.literal("}")
                rules.append((selector, body))
            except Exception:
                why = self.ignore_until(["}"])
                if why == "}":
                    self.literal("}")
                    self.white_space()
                else:
                    break
        return rules

def style(node, rules):
    # recursively parse the a node to get all the style attribute
    # of the node and its children and store it as the node attribute
    node.style = {}
    for key, default_value in INHERITED_PROPERTIES.items():
        if node.parent:
            node.style[key] = node.parent.style[key]
        else:
            node.style[key] = default_value
    for selector, body in rules:
        if not selector.matches(node): continue
        for key, value in body.items():
            node.style[key] = value
    if isinstance(node, Tag) and "style" in node.attributes:
        pairs = CSSParser(node.attributes["style"]).body()
        for key, value in pairs.items():
            node.style[key] = value
    if node.style["font-size"].endswith("%"):
        if node.parent:
            parent_font_size = node.parent.style["font-size"]
        else:
            parent_font_size = INHERITED_PROPERTIES["font-size"]
        node_pct = float(node.style["font-size"][:-1]) / 100
        parent_px = float(parent_font_size[:-2])
        node.style["font-size"] = f"{node_pct * parent_px}px"
    for child in node.children:
        style(child, rules)

class TagSelector:
    def __init__(self, tag, priority=1):
        self.tag = tag
        self.priority = priority

    def matches(self, node):
        return isinstance(node, Tag) and node.tag == self.tag

    def __repr__(self) -> str:
        return f"TagSelector(tag={self.tag}, priority={self.priority})"

class DescendantSelector:
    def __init__(self, ancestor, descendant):
        self.ancestor = ancestor
        self.descendant = descendant
        self.priority =  ancestor.priority + descendant.priority

    def matches(self, node):
        if not self.descendant.matches(node): return False
        while node.parent:
            if self.ancestor.matches(node.parent): return True
            node = node.parent
        return False
    
    def __repr__(self) -> str:
        return f"DescendantSelector(ancestor={self.ancestor}, descendant={self.descendant}, priority={self.priority})"
        