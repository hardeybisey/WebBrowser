import socket
import ssl
from abc import ABC, abstractmethod
import os
from pathlib import Path

class Base(ABC):
    @abstractmethod
    def request(self):
        pass
    
    def resolve(self, url):
        "Resolve a relative URL to an absolute one."
        if "://" in url: return  self.__class__(url)
        if not url.startswith("/"):
            _dir, _ = self.path.rsplit("/", 1)
            while url.startswith("../"):
                _, url = url.split("/", 1)
                if "/" in _dir:
                    _dir, _ = _dir.rsplit("/", 1)
            url = f"{_dir}/{url}"
        if url.startswith("//"):
            self.__class__(f"{self.scheme}:{url}")
        else:
            return self.__class__(f"{self.scheme}://{self.host}:{self.port}{url}")

class WebURL(Base):
    def __init__(self, host, path, port=80, scheme="http"):
        self.host = host
        self.path = path
        self.port = port
        self.scheme = scheme

    def request(self):
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        
        request = f"GET {self.path} HTTP/1.0\r\n"
        request +=f"Host: {self.host}\r\n"
        request += f"Connection: close\r\n"
        request += f"User-Agent: TKBrowserv\r\n"
        request += "\r\n"
        s.send(request.encode("utf8"))
        
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        self.statusline = response.readline()
        # version, status, explanation = self.statusline.split(" ", 2)
        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.lower()] = value.strip()
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        
        self.response_headers = response_headers
        
        content = response.read()
        s.close()
        return content
    
class FileURL(Base):
    def __init__(self, path):
        self.path = path
    
    def request(self):
        dir_list = "\n".join(f"<li>{d}</li>" for d in os.listdir())
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sample HTML</title>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="style.css" />
        </head>
        <body>
            <div> File List </div>
            <ul>
            {dir_list}
            </ul>
        </body>
        </html>
        """
        return content 
    
class URL(Base):
    scheme_mapping = {
        "http": 80,
        "https": 443,
    }
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        if self.scheme in ("http", "https"):
            parts = url.split("/", 1)
            self.host = parts[0]
            self.path = "/" + parts[1] if len(parts) > 1 else "/"
            self.port = self.scheme_mapping.get(self.scheme, 80)
            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port = int(port)
        elif self.scheme == "file":
            assert Path(url).exists() and Path(url).is_dir()
            self.path = url
            self.host = "localhost"
        # elif self.scheme == "raw":
        #     self.host = "localhost"
        #     self.path = url

    def request(self):
        if self.scheme in ("http", "https"):
            web_url = WebURL(self.host, self.path, self.port, self.scheme)
            return web_url.request()
        elif self.scheme == "file":
            file_url = FileURL(self.path)
            return file_url.request()
        else:
            raise ValueError(f"Unsupported URL scheme: {self.scheme}")
        
        
# class RawHtmlURL(Base):
#     def __init__(self, path):
#         self.path = path
    
#     def request(self):
#         content = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>Sample HTML</title>
#             <meta charset="UTF-8">
#             <link rel="stylesheet" href="style.css" />
#         </head>
#         <body>
#             <div> Raw HTML </div>
#             <pre>
#             {self.path}
#             </pre>
#         </body>
#         </html>
#         """
#         return content
