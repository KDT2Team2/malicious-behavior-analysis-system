from http.server import BaseHTTPRequestHandler, HTTPServer
import json

def exec_command(command):
    # 구현
    pass

def save_file(data, save_path) -> bool:
    try:
        with open(save_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f'{str(e)}')
        return False
    return True

def load_file(file_path) -> bytes:
    with open(file_path, 'rb') as f:
        data = f.read()
        return data

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, this is a GET request!')
        if self.path =='/download':
            # 구현
            # load_file 호출
            pass
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def do_POST(self):
    if self.path == '/command':
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode('utf-8'))
            response_data = {'message': 'Data received successfully', 'data': data}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Bad Request: Invalid JSON data')
    if self.path == '/upload':
        # 구현
        # save_file 호출
        pass
    else:
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'404 Not Found')

def run_server():
    address = ('0.0.0.0', 8080)
    with HTTPServer(address, MyRequestHandler) as server:
        print('Starting server...')
        server.serve_forever()

if __name__ == '__main__':
    run_server()