from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse

PORT = 8080

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("home.html", "rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/login":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("login.html", "rb") as file:
                self.wfile.write(file.read())
        elif self.path == "/user_home":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("user_home.html", "rb") as file:
                self.wfile.write(file.read())
        elif self.path.startswith("/static/"):
            file_path = self.path.lstrip("/")
            try:
                with open(file_path, "rb") as file:
                    self.send_response(200)
                    if file_path.endswith(".css"):
                        self.send_header("Content-type", "text/css")
                    elif file_path.endswith(".js"):
                        self.send_header("Content-type", "application/javascript")
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urlparse.parse_qs(post_data.decode('utf-8'))

            username = data.get("username", [None])[0]
            password = data.get("password", [None])[0]

            if username == "testuser" and password == "password":  # Simplified authentication check
                self.send_response(302)
                self.send_header("Location", "/user_home")
                self.end_headers()
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b"Invalid credentials")

httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
print(f"Serving on http://localhost:{PORT}")
httpd.serve_forever()
