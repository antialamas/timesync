#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class ParameterServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="src/public", **kwargs)

def run(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ParameterServer)
    print(f"Server running at http://localhost:{port}/parameter_input.html")
    httpd.serve_forever()

if __name__ == '__main__':
    run()