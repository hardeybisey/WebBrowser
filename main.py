from url import URL
from browser import Browser

def main():
    url= "https://browser.engineering/styles.html"
    url2 = "file:///Users/hardey/Desktop/WebBrowser"
    url = URL(url=url)
    browser = Browser()
    browser.load(url)
    browser.window.mainloop()
    

if __name__ == "__main__":
    main()