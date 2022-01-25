from main import app as application

from gevent.pywsgi import WSGIServer

HOST: str = '192.168.1.108'
PORT: int = 5437

print('\n\n\t...........Application is running...........\n\n\n')

http_server = WSGIServer((HOST, PORT), application)
http_server.serve_forever()
