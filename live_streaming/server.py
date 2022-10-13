# This code is for the server
# Lets import the libraries
import socket, cv2, pickle, struct, imutils
import numpy as np
from mss import mss
from PIL import Image
import json 

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

sct = mss()
sct.compression_level = 15
mon = sct.monitors[0]

def get_image_data():
    # Grab the data
    sct_img = sct.grab(mon)
    # sct.get_pixels(mon)
    # img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    return np.array(sct_img)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    try:
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            while True:
                image_data = get_image_data()

                image_bytes = pickle.dumps(image_data) #serialize frame to bytes
                delimeter = pickle.dumps('@')
                # print(message)
                try:
                    # client_socket.sendall(size_bytes)
                    # client_socket.sendall(pickle.dumps(":"))
                    print('sending imagewith size {}'.format(len(image_bytes)))
                    client_socket.sendall(image_bytes + delimeter) #send message or data frames to client
                except Exception as e:
                    print(e)
                    client_socket.close()
                    break 

                # cv2.imshow('TRANSMITTING VIDEO', image_data) # will show video frame on server side.
                # key = cv2.waitKey(1) & 0xFF
                # if key == ord('q'):
                #     client_socket.close()
    except Exception as e:
        pass 

    client_socket.close()
