import argparse
import socket
import shlex
import subprocess
import sys
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

class Netcat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
            
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen()
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket, ))
            client_thread.start()
            
    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        elif self.args.upload:
            file_buffer = ''
            while True:
                data = client_socket.recv(4069)
                if data:
                    file_buffer += data
                else:
                    break
            with open('recv_file.txt', 'wb') as f:
                f.write(file_buffer)
                
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP#> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64) 
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = ''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()
            
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
            
        try: 
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4069)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4069:
                        break
                if response:
                    print(response)
                    buffer = input(">   ")
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except EOFError:
            print("No more input. Closing connection")
            self.socket.close()
            sys.exit()
        except KeyboardInterrupt:
            print('User terminated')
            self.socket.close()
            sys.exit()
    
         

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Netcat by me", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute a command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='command shell')
    parser.add_argument('-t', '--target', default='192.168.0.1', help='command shell')
    parser.add_argument('-u', '--upload', help='command shell')
    args = parser.parse_args()
    
    buffer = None if args.listen else (sys.stdin.read() if not sys.stdin.isatty() else None)
    
    nc = Netcat(args, buffer.encode() if buffer else None)
    nc.run()