#client
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

msg = "h"
s.connect(("127.0.0.1", 7777))
s.send(msg.encode())
print(s.recv(10).decode())
s.close()
