import socket 
import threading

def sock_handle(client_socket):
    with client_socket as sock:
        while True:
            request = sock.recv(4069)
            print(request.decode("utf-8"))
            sock.send(b'hello client')
            if len(request) == 0:
                client_socket.close()
                break

IP = '0.0.0.0'
PORT = 9998

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((IP, PORT))
server.listen(5)

while True:
    client_socket, addr = server.accept()
    client_handle = threading.Thread(target=sock_handle, args=(client_socket,) )
    client_handle.start()
    
    