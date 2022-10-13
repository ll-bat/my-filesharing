import socket, pickle, struct
import cv2

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.1.1'  # paste your server ip address here
port = 9999
client_socket.connect((host_ip, port))  # a tuple

is_complete_image = False 
image_data_bytes = b''
image_data_bytes_list = []
delimeter = pickle.dumps('@')

while True:    
    while is_complete_image is False:
        received_data = client_socket.recv(4 * 1024)
        if not received_data:
            continue  
        image_data_bytes_list.append(received_data)
        if received_data.find(delimeter) >= 0:
            is_complete_image = True 
    
    last_part = image_data_bytes_list.pop()
    parts_list = last_part.split(delimeter)
    image_data_bytes_list.append(parts_list[0])

    try:
        image_data = pickle.loads(b''.join(image_data_bytes_list)) # de-serialize bytes into actual frame type
        print('pickled successfully')
    except Exception as e:
        print(image_data_bytes[-100:])
        print(len(parts_list[0]))
        print(str(e))
        break 

    cv2.imshow("RECEIVING VIDb';'EO", image_data) # show video frame at client side

    image_data_bytes_list = [delimeter.join(parts_list[1:])]
    if len(parts_list) > 2:
        is_complete_image = True 
    else:
        is_complete_image = False 

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): # press q to exit video
        break

client_socket.close()