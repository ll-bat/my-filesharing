import pickle
import traceback
import cv2

from core.server import Server
from core.config import Config
from core.helpers import BytesReceiver

server = Server(Config.host_ip, Config.port)
server.connect()

bytes_receiver = BytesReceiver(server) 
bytes_receiver_iter = iter(bytes_receiver)

while True:
    try:
        image_bytes = next(bytes_receiver_iter) 
        if not image_bytes:
            break 

        image_data = pickle.loads(image_bytes) 
        cv2.imshow("RECEIVING VIDb';'EO", image_data) # show video frame at client side

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # press q to exit video
            break

    except Exception as e:
        print(traceback.format_exception()) 
        break 

server.close_connection()