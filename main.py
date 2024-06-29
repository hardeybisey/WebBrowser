from url import URL
from browser import Browser

def main():
    url= "https://browser.engineering/"
    url1 = "https://browser.engineering/styles.html"
    url2 = "file:///Users/hardey/Desktop/WebBrowser"
    url = URL(url=url1)
    browser = Browser()
    browser.load(url)
    browser.root.mainloop()
    

if __name__ == "__main__":
    main()