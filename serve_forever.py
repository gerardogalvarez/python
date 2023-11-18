"""Ejemplo de serve_forever"""
import os
import json
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import time

data = {"message" : "hola mundo!"}

class FileUploadHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path.startswith("/echo"):
            message = '\n'.join(
                [
                    'CLIENT VALUES:',
                    'client_address=%s (%s)' % (self.client_address, self.address_string()),
                    'command=%s' % self.command,
                    'path=%s' % self.path,
                    'real path=%s' % parsed_path.path,
                    'query=%s' % parsed_path.query,
                    'request_version=%s' % self.request_version,
                    '',
                    'HEADERS:',
                    '%s' % self.headers,
                ]
            )
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))
        
        elif parsed_path.path.startswith("/redirect"):
            self.send_response(301)
            # self.send_header('Location', "/echo")
            self.end_headers()
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Página no encontrada')
        
            # BaseHTTPRequestHandler.do_GET(self)

        return
    
    def do_PUT(self):
        if self.path == '/api/data':
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')
            new_data = json.loads(put_data)
            data.update(new_data)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Página no encontrada')
    
    def do_POST(self):
        content_type = self.headers.get('Content-Type', 'application/json')
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        if content_type == 'application/json':
            post_data = json.loads(post_data)
            file_extension = post_data.get('fileExtension', content_type.split('/')[1])
            file_name = post_data.get('fileName',  'temp-' +  str(time()) + '.' + file_extension)
            file_path = os.path.join(os.getcwd(), file_name)
            with open(file_path, 'w') as f:
                if file_extension == 'json':
                  json.dump(json.loads(post_data.get('responseData')), f)
                else:
                  f.write(post_data)
        else:
          file_extension = content_type.split('/')[1]
          file_name = 'temp-' +  str(time()) + '.' + file_extension
          file_path = os.path.join(os.getcwd(), file_name)
          with open(file_path, 'wb') as f:
              f.write(post_data)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps({'filePath': file_path}), 'utf8'))

if __name__ == '__main__':
    with HTTPServer(('', 3000), FileUploadHandler) as server:
      print('Starting HTTP server...')
      server.serve_forever()