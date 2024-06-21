import socket
import ssl

class URL:
    scheme_mapping = {
        "http": 80,
        "https": 443,
    }
    def __init__(self, url):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ("http", "https")
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        self.port = self.scheme_mapping[self.scheme]
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)
    
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
        request += "\r\n"
        s.send(request.encode("utf8"))
        
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        
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