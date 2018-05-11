import io
import socket
import struct
from PIL import Image
import cv2
import numpy as np

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8003))
print("gay is jake")
server_socket.listen(0)
print("lisen done")
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
print("why is jake so gay")
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the

        # length is zero, quit the loop
        print("Check")
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        print("JAKEIS GAY")
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        cv_image = np.array(image)
        cv2.imshow('Stream',cv_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    connection.close()
    server_socket.close()
print("ded")
