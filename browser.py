import tkinter
import tkinter.font
from html_parser import HTMLParser
from layout import Layout


WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
FONTS = {}

        
class Browser:
    def __init__(self):
        self.scroll = 0
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window, 
            width=WIDTH,
            height=HEIGHT
        )
        # self.scrollbar = tkinter.Scrollbar(
        #     self.window,
        #     orient="vertical",
        #     command=self.canvas.yview
        # )
        # self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<MouseWheel>", self.scroll)
        self.canvas.pack(fill="both", expand=True)
        # self.scrollbar.pack(side=tkinter.RIGHT, fill="both")

    def draw(self):
        self.canvas.delete("all")
        for x, y, c, f in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f, anchor="nw")

    def load(self, url):
        body = url.request()
        self.nodes = HTMLParser(body).parse()
        self.display_list = Layout(self.nodes).display_list
        self.draw()
    
    def scroll(self, event):
        print("event.delta", event.delta)
        self.scroll += event.delta
        self.draw()
        

