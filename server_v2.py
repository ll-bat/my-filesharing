#SERVER
import os
import socket

s = socket.socket()
host = 'localhost'
port = 8080
s.bind((host, port))
print("Server started at: ", host)
s.listen(2)
conn,addr = s.accept()
print(addr, "connected")
