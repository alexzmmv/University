
import os
import socket
import sys
from time import sleep

port = int(sys.argv[1])
ip = sys.argv[2]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))

s.listen(1)

while True:
    conn, addr = s.accept()

    fork = os.fork()

    if fork == 0:  
        n1 = conn.recv(1024).decode()
        n2 = conn.recv(1024).decode()
        print(f"Received {n1} and {n2}")

        sum = int(n1) + int(n2)


        conn.send(str.encode(str(sum)))

        conn.close()
        os._exit(0)

    else:
        conn.close()
