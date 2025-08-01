import socket
import sys
import time

port = int(sys.argv[1])
ip= sys.argv[2]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

s.sendall(str.encode(input("Enter first number: ")))
time.sleep(0.1)

s.sendall(str.encode(input("Enter second number: ")))

msg = s.recv(1024)
print(msg.decode())

s.close()