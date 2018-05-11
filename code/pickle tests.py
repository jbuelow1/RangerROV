import pickle
import socket
import dill

s = socket.socket()
host = socket.gethostname()
port = 12341
s.bind((host,port))

s.listen(5)
while True:
    c, addr = s.accept()
    data1 = c.recv(1024)
    print(data1)
    
    print("Made connection with " + str(addr))
    c.send('kys'.encode(encoding='UTF-8'))
    c.close()

#def read(_socket):
 #   f = _socket.makefile('rb', buffer_size )
  #  data = pickle.load(f)
   # f.close()
    #return data

