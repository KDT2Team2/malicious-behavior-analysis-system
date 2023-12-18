from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import subprocess

def exec_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr.decode('utf-8')}"

def save_file(data, save_path) -> bool:
    try:
        with open(save_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f'{str(e)}')
        return False
    return True

def load_file(file_path) -> bytes:
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        return data
    except Exception as e:
        print(f'{str(e)}')
        return None

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, this is a GET request!')
        elif self.path.startswith('/download'):
            file_name = self.path.split('/')[-1]
            file_data = load_file(file_name)
            if file_data:
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(file_data)
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'File not found')
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
                command_output = exec_command(data['command'])
                response_data = {'output': command_output}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Bad Request: Invalid JSON data')
        elif self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            file_name = self.headers['X-File-Name']
            file_data = self.rfile.read(content_length)
            if save_file(file_data, file_name):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'File uploaded successfully')
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Internal Server Error')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run_server():
    # 가상환경 ip 주소
    address = ('10.0.2.15', 8080)
    with HTTPServer(address, MyRequestHandler) as server:
        print('Starting server...')
        server.serve_forever()

if __name__ == '__main__':
    run_server()
