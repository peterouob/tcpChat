import socketserver, sys, threading
from time import ctime


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('[%s] Client connected from %s ' % (
            ctime(), self.request.getpeername()))
        while True:
            indata = self.request.recv(1024).strip()
            if len(indata) == 0:  # connection closed
                self.request.close()
                print('client closed connection.')
                break
            print(str(self.request.getpeername()) + '：' + indata.decode())

            outdata = 'echo ' + indata.decode()
            self.request.send(outdata.encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    HOST, PORT = '0.0.0.0', 7777
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    print('server start at: %s:%s' % (HOST, PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
