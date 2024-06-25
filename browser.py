import tkinter as tk
import tkinter.font as tkFont
from html_parser import HTMLParser
from layout import DocumentLayout, paint_tree
from css_parser import style


WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
FONTS = {}

        
class Browser:
    "A simple web browser."
    def __init__(self):
        self.scroll_pos = 0
        self.width = WIDTH
        self.height = HEIGHT
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window, 
            width=WIDTH,
            height=HEIGHT
        )
        # self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.window.bind("<MouseWheel>", self.scroll)
        # self.window.bind("<Configure>", self.resize)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
        self.node = HTMLParser(body).parse()
        style(self.node)
        self.document = DocumentLayout(self.node)
        self.document.layout()
        self.display_list = []
        paint_tree(self.document, self.display_list)
        # for i in self.display_list[-20:]:
        #     print(i)
        self.draw()
    
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