import tkinter
import tkinter.font

from models import Text, Tag, ClosingTag, SelfClosingTag

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
# SCROLL_STEP = 100

FONTS = {}

def get_font(size, weight, style):
    "Return a font object with the given attributes."
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(
            size=size, 
            weight=weight,
            slant=style
            )
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]

class Layout:
    "Lay out the nodes in a tree structure."
    def __init__(self, node:Tag):
        self.nodes = node
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 12
        self.line = []
        self.counter = 0 
        self.recurse(node)
        
    def open_tag(self, tag:str):
        "Handle an opening tag."
        if tag == "i":
            self.style = 'italic'
        elif tag == "b":
            self.weight = 'bold'
        elif tag == "small":
            self.size -= 2     
        elif tag == "big":
            self.size += 4
        # elif tag == "p":
        #     self.flush()
        #     self.cursor_y+=VSTEP
        elif tag == "br":
            self.flush()        
        
    def close_tag(self, tag:str):
        "Handle a closing tag."
        if tag == "/i":
            self.style = 'roman'
        elif tag == "/b":
            self.weight = 'normal'
        elif tag == "/small":
            self.size += 2
        elif tag == "/big":
            self.size -= 4
        elif tag == "/p":
            self.flush()
            self.cursor_y+=VSTEP
            
    def recurse(self, node:Tag):
        "Recurse through the tree adding open and close tags as needed."
        while node.next:
            if isinstance(node, (Tag, SelfClosingTag)):
                self.open_tag(node.tag)
                if isinstance(node.text, Text):
                    for word in node.text.text.split():
                        self.word(word)
            if isinstance(node, ClosingTag):
                self.close_tag(node.tag)
            node = node.next

    def word(self, word:str):
        "Add words to the current line."
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")
        if self.cursor_x + w > WIDTH - HSTEP:
            self.flush()
            
    def flush(self):
        "Flush the current line and start a new one."
        if not self.line: return
        metrics = [font.metrics() for _, _, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = HSTEP
        self.line = []