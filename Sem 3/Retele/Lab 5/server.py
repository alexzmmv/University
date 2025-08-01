import socket
import sys


port = int(sys.argv[1])
ip = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))

s.listen(1)

conn, addr = s.accept()

n1 = conn.recv(1024).decode()

n2 = conn.recv(1024).decode()

print(f"Received {n1} and {n2}")
sum = int(n1) + int(n2)


conn.send(str.encode(str(sum)))