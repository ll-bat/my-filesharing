# This code is for the server
# Lets import the libraries
import socket, cv2, pickle, struct, imutils
import numpy as np
from mss import mss
from PIL import Image

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(1)
print("LISTENING AT:", socket_address)

mon = {'top': 0, 'left': 0, 'width': 100, 'height': 100}
sct = mss()

def get_image_data():
    sct.get_pixels(mon)
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    return np.array(img)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        while True:
            image_data = get_image_data()
            
            a = pickle.dumps(image_data) #serialize frame to bytes
            message = struct.pack("Q", len(a)) + a # pack the serialized data
            # print(message)
            try:
                client_socket.sendall(message) #send message or data frames to client
            except Exception as e:
                print(e)
                raise Exception(e)


            cv2.imshow('TRANSMITTING VIDEO', image_data) # will show video frame on server side.
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
