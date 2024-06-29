import tkinter as tk
from html_parser import HTMLParser
from layout import DocumentLayout, paint_tree
from css_parser import style, CSSParser
from models import Tag
from utils import tree_to_list

DEFAULT_STYLE_SHEET = CSSParser(open("static/browser.css").read()).parse()
print(DEFAULT_STYLE_SHEET)
WIDTH, HEIGHT = 800, 700
HSTEP, VSTEP = 13, 18
FONTS = {}

        
class Browser:
    "A simple web browser."
    def __init__(self):
        self.scroll_pos = 0
        self.width = WIDTH
        self.height = HEIGHT
        self.root = tk.Tk()
        self.root.title("Dummy Browser")
        
        self.hscrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.hscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.vscrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.vscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(
            self.root, 
            width=WIDTH,
            height=HEIGHT,
            bg="white",
            yscrollcommand=self.hscrollbar.set,
            xscrollcommand=self.vscrollbar.set,
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.hscrollbar.config(command=self.canvas.yview)
        self.vscrollbar.config(command=self.canvas.xview)
        self.root.bind("<MouseWheel>", self.scroll)
        # self.window.bind("<Configure>", self.resize)

    def draw(self):
        "Draw the display list."
        self.canvas.delete("all")
        for cmd in self.display_list:
            if cmd.top > self.scroll_pos + HEIGHT: continue
            if cmd.bottom < self.scroll_pos: continue
            cmd.execute(self.scroll_pos, self.canvas)

    def load(self, url):
        "Load the given URL and display it in the window."
        body = url.request()
        # body = """
        # <!DOCTYPE html>
        # <html>
        # <head>
        #     <title>My Page</title>
        # </head>
        # <body>
        # <style background-color: blue; color: white; font-size: 16px;>
        #     <div>
        #         Hello World
        #     </div>
        #     <div> 
        #         <p> <i>This is a paragraph </i></p>
        #         <a href="https://www.google.com"> This is a link </a>
        #     </div>
        # </body>
        # </html>
        # """
        rules = DEFAULT_STYLE_SHEET.copy()
        self.node = HTMLParser(body).parse()
        links = [node.attributes["href"] for node in tree_to_list(self.node, []) if isinstance(node, Tag) and "href" in node.attributes and node.attributes.get("rel") == "stylesheet"]
        for link in links:
            style_url = url.resolve(link)
            try:
                body = style_url.request()
            except Exception:
                continue
            rules.extend(CSSParser(body).parse())
        style(self.node, sorted(rules, key=lambda x: x[0].priority))
        self.document = DocumentLayout(self.node)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        self.draw()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def scroll(self, event):
        "Scroll through the display list."
        new_scroll_pos = self.scroll_pos + event.delta
        if new_scroll_pos < 0:
            self.scroll_pos =0 
        elif new_scroll_pos > self.document.height - self.height:
            self.scroll_pos = self.document.height - self.height
        else:
            self.scroll_pos = new_scroll_pos
        self.draw()
        
    # def resize(self, event):
    #     print(event.__dict__)
    #     self.width = event.width
    #     self.height = event.height
    #     self.display_list = []
    #     self.document.layout()
        # paint_tree(self.document, self.display_list)
        # self.draw()