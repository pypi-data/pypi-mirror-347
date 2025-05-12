# pyvenDF/server.py

import socket
import os
import sys
import select
import time
from pyvenDF.router import Router
from pyvenDF.templates.routes import routes  # user-defined routes from project template

MIME_TYPES = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".txt": "text/plain",
    ".pdf": "application/pdf",
}

def get_content_type(file_path):
    """Determine the content type based on file extension."""
    _, ext = os.path.splitext(file_path)
    return MIME_TYPES.get(ext, "application/octet-stream")

def start_server(host='127.0.0.1', port=8080):
    """Start the server, handling incoming requests and matching routes."""
    router = Router()
    for route in routes:
        router.add_route(route["pattern"], route["handler"])

    sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_conn.bind((host, port))
    sock_conn.listen(5)
    sock_conn.setblocking(False)

    print(f"🚀 Pyven server running at http://{host}:{port}")

    try:
        while True:
            try:
                # Check for new incoming connections
                ready_to_read, _, _ = select.select([sock_conn], [], [], 1.0)
                if sock_conn in ready_to_read:
                    client_sock, client_addr = sock_conn.accept()
                    client_sock.settimeout(1.0)
                    print(f"📡 Connected from {client_addr}")

                    try:
                        # Receive the HTTP request
                        request = client_sock.recv(1024).decode('utf-8')
                    except socket.timeout:
                        client_sock.close()
                        continue

                    if not request:
                        client_sock.close()
                        continue

                    parts = request.split()
                    if len(parts) < 2:
                        client_sock.close()
                        continue

                    method, path = parts[0], parts[1]
                    if path == "/":
                        path = "/index.html"

                    file_path = "." + path

                    # Try to serve static file
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as f:
                            content = f.read()
                        content_type = get_content_type(file_path)
                        response = b"HTTP/1.1 200 OK\r\n"
                        response += f"Content-Type: {content_type}\r\n".encode()
                        response += b"Content-Length: " + str(len(content)).encode() + b"\r\n\r\n"
                        response += content
                        status_code = "200 OK"
                    else:
                        # Try to match routes
                        handler, params = router.match(path)
                        if handler:
                            body = handler(**params).encode()
                            response = b"HTTP/1.1 200 OK\r\n"
                            response += b"Content-Type: text/html\r\n"
                            response += b"Content-Length: " + str(len(body)).encode() + b"\r\n\r\n"
                            response += body
                            status_code = "200 OK"
                        else:
                            body = b"<h1>404 Not Found</h1>"
                            response = b"HTTP/1.1 404 Not Found\r\n"
                            response += b"Content-Type: text/html\r\n"
                            response += b"Content-Length: " + str(len(body)).encode() + b"\r\n\r\n"
                            response += body
                            status_code = "404 Not Found"

                    # Send response to client
                    client_sock.sendall(response)
                    client_sock.close()

                    print(f"[{time.strftime('%d/%b/%Y %H:%M:%S')}] \"{method} {path}\" {status_code}")

            except KeyboardInterrupt:
                print("\n🛑 Shutting down gracefully...")
                sock_conn.close()
                sys.exit()

    except Exception as e:
        print(f"❌ Server error: {e}")
        sock_conn.close()
        sys.exit()
