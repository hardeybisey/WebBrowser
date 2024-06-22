import tkinter
import tkinter.font
from html_parser import HTMLParser
from layout import Layout


WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
FONTS = {}

        
class Browser:
    "A simple web browser."
    def __init__(self):
        self.scroll_pos = 0
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window, 
            width=WIDTH,
            height=HEIGHT
        )
        self.window.bind("<MouseWheel>", self.scroll)
        self.canvas.pack(fill="both", expand=True)

    def draw(self):
        "Draw the display list."
        self.canvas.delete("all")
        for x, y, c, f in self.display_list:
            if y > self.scroll_pos + HEIGHT: continue
            if y + VSTEP < self.scroll_pos: continue
            self.canvas.create_text(x, y - self.scroll_pos, text=c, font=f, anchor="nw")

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
        self.nodes = HTMLParser(body).parse()
        self.display_list = Layout(self.nodes).display_list
        self.draw()
    
    def scroll(self, event):
        "Scroll through the display list."
        self.scroll_pos += event.delta
        self.draw()
        

