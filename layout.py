import tkinter
import tkinter.font

from models import Text, Tag, ClosingTag, SelfClosingTag


BLOCK_ELEMENTS = [
    "html", "body", "article", "section", "nav", "aside",
    "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "header",
    "footer", "address", "p", "hr", "pre", "blockquote",
    "ol", "ul", "menu", "li", "dl", "dt", "dd", "figure",
    "figcaption", "main", "div", "table", "form", "fieldset",
    "legend", "details", "summary"
] 
    
WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18

FONTS = {}

def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())
    for child in layout_object.children:
        paint_tree(child, display_list)

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

class BlockLayout:
    def __init__(self, node, parent, previous):
        self.node = node
        self.parent = parent
        self.previous = previous
        self.children = []
        self.display_list = []
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self._layout_mode()

    def __repr__(self):
        return "BlockLayout[{}]:(layout={},x={},y={},height={},width={})".format(self.node,self.layout_mode,self.x,self.y,self.height,self.width)

    def layout(self):
        self.x = self.parent.x
        self.width = self.parent.width
        if self.previous:
            self.y = self.previous.y + self.previous.height
        else:
            self.y = self.parent.y
        if self.layout_mode == "block":
            self.layout_block()
        else:
            self.cursor_x = 0
            self.cursor_y = 0
            self.weight = "normal"
            self.style = "roman"
            self.size = 12
            
            self.line = []
            self.recurse(self.node)
            self.flush()
            
        for child in self.children:
            child.layout()
            
        if self.layout_mode == "block":
            self.height = sum([child.height for child in self.children])
        else:
            self.height = self.cursor_y

    def layout_block(self):
        previous = None
        for child in self.node.children:
            current = BlockLayout(node=child, parent=self, previous=previous)
            self.children.append(current)
            previous = current
            
    def _layout_mode(self):
        if isinstance(self.node, Text):
            self.layout_mode = "inline"
        elif any([isinstance(child, (Tag,ClosingTag)) and child.tag in BLOCK_ELEMENTS for child in self.node.children]):
            self.layout_mode= "block"
        elif self.node.children:
            self.layout_mode = "inline"
        else:
            self.layout_mode = "block"
        
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
        
    def recurse(self, node):
        "Recurse through the tree adding open and close tags as needed."
        if isinstance(node, Text):
            for word in node.text.split():
                self.word(word)
        else:
            if isinstance(node, (Tag, SelfClosingTag)):
                self.open_tag(node.tag)
            for child in node.children:
                self.recurse(child)
            if isinstance(node, ClosingTag):
                self.close_tag(node.tag)

    def word(self, word:str):
        "Add words to the current line."
        font = get_font(self.size, self.weight, self.style)
        w = font.measure(word)
        if self.cursor_x + w > self.width:
            self.flush()
        self.line.append((self.cursor_x, word, font))
        self.cursor_x += w + font.measure(" ")
            
    def flush(self):
        "Flush the current line and start a new one."
        if not self.line: return
        metrics = [font.metrics() for _, _, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for rel_x, word, font in self.line:
            x = self.x + rel_x
            y = self.y + baseline - font.metrics("ascent")
            self.display_list.append((x, y, word, font))
        self.cursor_x = 0
        self.line = []
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
    
    def paint(self):
        cmds = []
        if self.layout_mode == "inline":
            for x, y, text, font in self.display_list:
                cmds.append(DrawText(x, y, text, font))
            
        if isinstance(self.node, (Tag, SelfClosingTag)) and self.node.tag == "pre":
            x2, y2 = self.x + self.width, self.y + self.height
            cmds.append(DrawRect(self.x, self.y, x2, y2, "gray"))
        return cmds
        
class DocumentLayout:
    def __init__(self, node):
        self.node = node
        self.parent = None
        self.previous = None
        self.children = []
        
    def layout(self):
        child = BlockLayout(node=self.node, parent=self, previous=None)
        self.children.append(child)
        self.width = WIDTH - 2 * HSTEP
        self.x = HSTEP
        self.y = VSTEP
        child.layout()
        self.height = child.height
        
    def paint(self):
        return []
    
    def __repr__(self):
        return "DocumentLayout[{}]:(x={},y={},height={},width={})".format(self.node,self.x,self.y,self.height,self.width)


class DrawText:
    def __init__(self, x1, y1, text, font):
        self.top = y1
        self.left = x1
        self.text = text
        self.font = font
        self.bottom = y1 + font.metrics("linespace")
    
    def execute(self, scroll, canvas):
        canvas.create_text(
            self.left, 
            self.top - scroll, 
            text=self.text, 
            font=self.font, 
            anchor="nw"
        )
class DrawRect:
    def __init__(self, x1, y1, x2, y2, color):
        self.top = y1
        self.left = x1
        self.bottom = y2
        self.right = x2
        self.color = color
        
    def execute(self, scroll, canvas):
        canvas.create_rectangle(
            self.left, 
            self.top - scroll, 
            self.right, 
            self.bottom - scroll, 
            width = 0,
            fill=self.color
        )