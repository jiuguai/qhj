import socket


sock1 = socket.socket()
sock2 = socket.socket()
sock3 = socket.socket()

print(sock1.fileno())
print(sock2.fileno())
print(sock3.fileno())

