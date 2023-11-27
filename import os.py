import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import time

class FileUploadHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_type = self.headers.get('Content-Type', 'application/json')
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        print('Receiving...' + content_type)
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
    
    def serve_forever(self):
        print('Listening in port 3000...');        

if __name__ == '__main__':
    with HTTPServer(('', 3000), FileUploadHandler) as server:
      print('Starting HTTP server...')
      server.serve_forever()
      print('Listening in port 3000...')