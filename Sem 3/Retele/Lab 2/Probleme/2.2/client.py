#client
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 7777))

lista_cuvinte=['ana','are','mere']
message=','.join(lista_cuvinte)
s.send(message.encode())
print(s.recv(10).decode())
s.close()
