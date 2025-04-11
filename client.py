import socket

ip = '172.25.142.113'
port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

while True:
    s = input()
    if not s:
        break
    
    client.send(s.encode())
    print((client.recv(4069)).decode())
        
    

client.close()