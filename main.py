from url import URL
from browser import Browser

def main():
    # url = "https://browser.engineering/"
    url= "https://browser.engineering/html.html"
    # url = "https://browser.engineering/examples/example2-rtl.html"
    url = URL(url=url)
    browser = Browser()
    browser.load(url)
    browser.window.mainloop()
    

if __name__ == "__main__":
    main()