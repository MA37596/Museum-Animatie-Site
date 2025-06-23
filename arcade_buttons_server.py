from gpiozero import Button
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import os

# Zorg ervoor dat we root-rechten hebben voor GPIO
if os.geteuid() != 0:
    print("Dit script moet met sudo worden uitgevoerd!")
    print("Probeer: sudo python3 arcade_buttons_server.py")
    exit(1)

# GPIO pins voor de knoppen
button1 = Button(17, pull_up=True)
button2 = Button(27, pull_up=True)
button3 = Button(22, pull_up=True)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/button':
            try:
                if button1.is_pressed:
                    button = 'video1'
                elif button2.is_pressed:
                    button = 'video2'
                elif button3.is_pressed:
                    button = 'video3'
                else:
                    button = None

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'button': button}).encode())
            except Exception as e:
                print(f"GPIO leesfout: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print('Server stopped.')

if __name__ == '__main__':
    print('Server starting... Press Ctrl+C to stop.')
    run()