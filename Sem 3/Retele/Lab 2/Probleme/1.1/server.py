import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 7777))
s.listen()
cs,addr=s.accept()
b=cs.recv(10).decode()
b*=2
cs.send(b.encode())
cs.close()