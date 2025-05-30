import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

class Server (paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
        
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username == 'atak') and (password == 'atak'):
            return paramiko.AUTH_SUCCESSFUL
        
if __name__ == '__main__':
    server = '192.168.56.1'
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('Listening for connections')
        client_socket, addr = sock.accept()
    except Exception as e:
        print(e)
        sys.exit(0)
    else:
        print('Connection!', client_socket, addr)
        
    bhSession = paramiko.Transport(client_socket)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)
    
    chan = bhSession.accept(20)
    if chan is None:
        print('*** no channel')
        sys.exit(0)
        
    print('Authenticated')
    print(chan.recv(1024))
    chan.send('Welcome to ssh')
    try:
        while True:
            command = input('Enter command: ')
            if command != 'exit':
                chan.send(command)
                r = chan.recv(1024)
                print(r.decode())
            else:
                chan.send('exit')
                print('Exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()
        
        