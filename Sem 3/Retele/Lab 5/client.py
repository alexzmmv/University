import socket
import sys
import time

port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("davidgatea.ddns.net", port))

s.sendall(str.encode("15"))
time.sleep(0.1)

s.sendall(str.encode("3"))

msg = s.recv(1024)
print(msg.decode())

s.close()