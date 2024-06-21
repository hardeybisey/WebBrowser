from url import URL

SELF_CLOSING_TAGS = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]

HEAD_TAGS = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script",
    ]

class Element:
    def __init__(self, tag, attributes, parent=None) -> None:
        self.tag = tag
        self.attributes = attributes
        self.prev = parent
        self.next = None
        self.text = ""
        self.closed = False
        
    def __repr__(self):
        return f"<{self.tag}>"

class Text:
    def __init__(self, text) -> None:
        self.text = text
        
    def __repr__(self):
        return f"{self.text}"
        

class HTMLParser:
    SELF_CLOSING_TAGS = [
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    ]

    HEAD_TAGS = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script",
    ]
    def __init__(self, body):
        self.body = body
        self.unfinished = []
        self.last_closed_tag = None
        
    def add_text(self, text):
        if text.isspace(): 
            return
        # self.implicit_tags(None)
        parent = self.unfinished[-1]
        parent.text = Text(text)
        
    def add_tag(self, tag):
        tag, attributes = self.get_attribute(tag)
        parent = self.unfinished[-1] if self.unfinished else None
        if tag.startswith("!"): 
            return
        elif tag.startswith("/"):
            if len(self.unfinished) == 1: 
                return
            tmp = self.unfinished.pop()
            tmp.closed = True
            if not tmp.next:
                self.last_closed_tag = tmp
        elif tag in self.SELF_CLOSING_TAGS:
            node = Element(tag, attributes=attributes, parent=parent)
            node.closed = True
            parent.next = node
        else:
            parent = self.last_closed_tag if self.last_closed_tag else parent
            self.last_closed_tag = None
            node = Element(tag, attributes=attributes, parent=parent)
            if parent: parent.next = node
            self.unfinished.append(node)
        # self.implicit_tags(tag)
            
    def finish(self):
        return self.unfinished[0]
        # # if not self.unfinished:
        # #     self.implicit_tags(None)
        # while len(self.unfinished) > 1:
        #     node = self.unfinished.pop()
        #     node.closed = True
        #     # parent = self.unfinished[-1]
        #     # parent.children.append(node)
        # return self.unfinished.pop()
        
    def get_attribute(self, text):
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
    
    def implicit_tags(self, tag):
        while True:
            open_tags = [node.tag for node in self.unfinished]
            if open_tags == [] and tag != "html":
                self.add_tag("html")
            elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
                if tag in self.HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
            elif open_tags == ["html", "head"] and tag not in ["/head"] + self.HEAD_TAGS:
                self.add_tag("/head")
            else:
                break
        

# count = 0

# def print_tree(node, indent=0):
#     global count
#     count+=1
#     print(" " * indent, node)
#     for child in node.children:
#         if count==10:
#             break
#         print_tree(child, indent + 2)

# body = URL(url="https://browser.engineering/text.html").request()
# parser = HTMLParser(body)
# nodes = parser.parse()
# # print_tree(nodes)











# from url import URL

# SELF_CLOSING_TAGS = [
#     "area", "base", "br", "col", "embed", "hr", "img", "input",
#     "link", "meta", "param", "source", "track", "wbr",
# ]

# HEAD_TAGS = [
#         "base", "basefont", "bgsound", "noscript",
#         "link", "meta", "title", "style", "script",
#     ]

# class Text:
#     def __init__(self, text, parent=None):
#         self.text = text
#         self.parent = parent
#         self.children = []
        
#     def __repr__(self):
#         return f"{self.text}"

# class Element:
#     def __init__(self, tag, attributes , parent=None):
#         self.tag = tag
#         self.attributes = attributes
#         self.parent = parent
#         self.children = []

#     def __repr__(self):
#         return f"<{self.tag}>"


# class HTMLParser:
#     SELF_CLOSING_TAGS = [
#         "area", "base", "br", "col", "embed", "hr", "img", "input",
#         "link", "meta", "param", "source", "track", "wbr",
#     ]

#     HEAD_TAGS = [
#         "base", "basefont", "bgsound", "noscript",
#         "link", "meta", "title", "style", "script",
#     ]
#     def __init__(self, body):
#         self.body = body
#         # self.head = None
#         self.unfinished = []
        
#     def add_text(self, text):
#         if text.isspace(): 
#             return
#         self.implicit_tags(None)
#         parent = self.unfinished[-1]
#         node = Text(text, parent=parent)
#         parent.children.append(node)
        
#     def add_tag(self, tag):
#         tag, attributes = self.get_attribute(tag)
#         parent = self.unfinished[-1] if self.unfinished else None
#         if tag.startswith("!"): 
#             return
#         elif tag.startswith("/"):
#             if len(self.unfinished) == 1: 
#                 return
#             node = self.unfinished.pop()
#             parent = self.unfinished[-1]
#             parent.children.append(node)
            
#         elif tag in self.SELF_CLOSING_TAGS:
#             node = Element(tag, attributes=attributes, parent=parent)
#             parent.children.append(node)
#         else:
#             node = Element(tag, attributes=attributes, parent=parent)
#             if parent: parent.children.append(node)
#             self.unfinished.append(node)
#         self.implicit_tags(tag)
            
#     def finish(self):
#         # return self.unfinished[0]
#         if not self.unfinished:
#             self.implicit_tags(None)
#         while len(self.unfinished) > 1:
#             node = self.unfinished.pop()
#             parent = self.unfinished[-1]
#             parent.children.append(node)
#         return self.unfinished.pop()
        
#     def get_attribute(self, text):
#         parts = text.split()
#         tag = parts[0].casefold()
#         attributes = {}
#         for attrpair in parts[1:]:
#             if "=" in attrpair:
#                 key, value = attrpair.split("=", 1)
#                 if value[0] in ('"', "'") and len(value) > 2:
#                     value = value[1:-1]
#                 attributes[key.casefold()] = value
#             else:
#                 attributes[attrpair.casefold()] = ""
#         return tag, attributes

#     def parse(self):
#         text = ""
#         in_tag = False
#         for token in self.body:
#             if token == "<":
#                 in_tag = True
#                 if text:
#                     self.add_text(text)
#                     text = ""
#             elif token == ">":
#                 in_tag = False
#                 self.add_tag(text)
#                 text = ""
#             else:
#                 text += token
#         if not in_tag and text:
#             self.add_text(text)
#         return self.finish()
    
#     def implicit_tags(self, tag):
#         while True:
#             open_tags = [node.tag for node in self.unfinished]
#             if open_tags == [] and tag != "html":
#                 self.add_tag("html")
#             elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
#                 if tag in self.HEAD_TAGS:
#                     self.add_tag("head")
#                 else:
#                     self.add_tag("body")
#             elif open_tags == ["html", "head"] and tag not in ["/head"] + self.HEAD_TAGS:
#                 self.add_tag("/head")
#             else:
#                 break
        

# # count = 0

# # def print_tree(node, indent=0):
# #     global count
# #     count+=1
# #     print(" " * indent, node)
# #     for child in node.children:
# #         if count==10:
# #             break
# #         print_tree(child, indent + 2)

# # body = URL(url="https://browser.engineering/text.html").request()
# # parser = HTMLParser(body)
# # nodes = parser.parse()
# # # print_tree(nodes)
