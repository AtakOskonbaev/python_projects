import sys
import socket
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
)

def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()
        
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        
        printable = word.translate(HEX_FILTER)
        hexa = ''.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results
    
    
def receive_from(socket):
    buffer = b''
    socket.settimeout(1)
    try:
        while True:
            data = socket.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    remote_buffer = b''
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
            hexdump(remote_buffer)
    
    if len(remote_buffer):
        print('sending data to localhost')
        
    while True:
        try:
            local_buffer = receive_from(client_socket)
            if len(local_buffer):
                print('sending data to remote host')
                hexdump(local_buffer)
            
                remote_socket.send(local_buffer)
                
            remote_buffer = receive_from(remote_socket)
            if len(remote_buffer):
                print('sending data to localhost')
                hexdump(remote_buffer)
                
                client_socket.send(remote_buffer)
                
            if not len(remote_buffer) and not len(local_buffer):
                print('no data to send and receieve')
                sys.exit(0)
        except KeyboardInterrupt as e:
            print("killed by ctrl c")
            sys.exit(0)
    

def server_loop(local_host, local_port,
                remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("Cannot bind on %s:%s" % (local_host, local_port))
        print(f'server killed {e}')
        sys.exit(0)
    server.listen(5)
    print(f'listening on {local_host}:{local_port}')
    while True:
        connection, addr = server.accept()
        print(f'recieved connection on {addr[0]}:{addr[1]}')
        proxy_handle = threading.Thread(target=proxy_handler, args=(connection, remote_host, remote_port, receive_first))
        proxy_handle.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]
    
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)
    
if __name__ == '__main__':
    main()