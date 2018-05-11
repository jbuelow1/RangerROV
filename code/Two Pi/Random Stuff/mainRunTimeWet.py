import neededIO as rovSTD
import pickle
import socket

mainSocket = socket.socket()
host = socket.gethostname()
port = 12332
mainSocket.bind((host, port))

mainSocket.listen(5)
client, address = mainSocket.accept()
print("Made connection with", address)
client.send("Connection made".encode('utf-8'))
while True:
    motorTimeHigh = pickle.loads(client.recv(1024))
    print(motorTimeHigh)
client.close()
