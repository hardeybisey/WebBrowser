from models import Text, OpenTag, CloseTag


conversion = {
    "&lt;": "<",
    "&gt;": ">",
    "&amp;": "&",
    "&quot;": '"',
    "&apos;": "'",
    "&euro;": "€",
    "&pound;": "£",
}
class HTMLParser:
    SELF_CLOSING_TAGS = [
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    ]

    HEAD_TAGS = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script",
    ]
    
    def __init__(self, body:str) -> None:
        self.body = body
        self.root = None
        self.current_node = None

    def add_text(self, text):
        "Add text to the current node."
        if text.isspace(): 
            return
        for key, value in conversion.items():
            if key in text:
                text = text.replace(key, value) 
        self.current_node.children.append(Text(text, parent=self.current_node))

    def add_tag(self, tag):
        "Add a tag to the current node."
        tag, attributes = self.get_attribute(tag)
        if tag.startswith("!"):
            return
        if tag.startswith("/"):
            node = CloseTag(tag, attributes=attributes, parent=self.current_node)
            self.current_node.children.append(node)
            self.current_node = self.current_node.parent
        elif tag in self.SELF_CLOSING_TAGS:
            node = OpenTag(tag, attributes=attributes, parent=self.current_node)
            self.current_node.children.append(node)
        else:
            node = OpenTag(tag, attributes=attributes, parent=self.current_node)
            if self.current_node:
                self.current_node.children.append(node)
            else:
                self.root = node
            self.current_node = node
        # self.implicit_tags(tag)
            
    def finish(self):
        "Return the root node."
        return self.root
        
    def get_attribute(self, text:str):
        "Parse a tag and return the tag name and attributes."
        parts = text.split()
        tag = parts[0].casefold()
        attributes = {}
        for attrpair in parts[1:]:
            if "=" in attrpair:
                key, value = attrpair.split("=", 1)
                if value[0] in ('"', "'") and len(value) > 2:
                    value = value[1:-1]
                attributes[key.casefold()] = value
            else:
                attributes[attrpair.casefold()] = ""
        return tag, attributes

    def parse(self):
        "Parse the HTML body into a tree and return the root node."
        text = ""
        in_tag = False
        for token in self.body:
            if token == "<":
                in_tag = True
                if text:
                    self.add_text(text)
                    text = ""
            elif token == ">":
                in_tag = False
                self.add_tag(text)
                text = ""
            else:
                text += token
        if not in_tag and text:
            self.add_text(text)
        return self.finish()
    
    # def implicit_tags(self, tag:str):
    #     "Add implicit tags as needed."
    #     while True:
    #         open_tags = [node.tag for node in self.node_list]
    #         if open_tags == [] and tag != "html":
    #             self.add_tag("html")
    #         elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
    #             if tag in self.HEAD_TAGS:
    #                 self.add_tag("head")
    #             else:
    #                 self.add_tag("body")
    #         elif open_tags == ["html", "head"] and tag not in ["/head"] + self.HEAD_TAGS:
    #             self.add_tag("/head")
    #         else:
    #             break