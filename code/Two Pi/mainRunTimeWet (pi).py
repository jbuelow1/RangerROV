import neededIO as rovSTD
import pickle
import socket
import picamera
import time

#Setup for sockets to send and recieve data
mainSocket = socket.socket()
secoundSocket = socket.socket()
host = '0.0.0.0'
port = 12334
mainSocket.bind((host, port))
print("Ready")
mainSocket.listen(5)
client, address = mainSocket.accept()
print("Made connection with", address)
client.send("Connection made".encode('utf-8'))
secoundSocket.bind((host, 8003))
secoundSocket.listen(5)
client2, address2 = secoundSocket.accept()
client.send("Connection made".encode('utf-8'))
connection = secoundSocket.accept()[0].makefile('wb')
with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        # Start a preview and let the camera warm up for 2 seconds
        #camera.start_preview()
        time.sleep(2)
        # Start recording, sending the output to the connection for 60
        # seconds, then stop
        camera.start_recording(connection, format='h264')

done = False
#Main runtime
while not done:
    #Receive pickle
    motorTimeHigh = pickle.loads(client.recv(1024))
    print(motorTimeHigh)

client.close()
client2.close()
