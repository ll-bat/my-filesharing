import pickle, traceback
from core.server import Server
from core.config import Config
from core.helpers import ScreenshotHelper, Helper

server = Server(Config.host_ip, Config.port)
server.start_server() 
server.wait_for_connections(1)

screenshot_helper = ScreenshotHelper()

# Socket Accept
client_socket, addr = server.get_connection()
try:
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        while True:
            image_data = screenshot_helper.get_screenshot()

            image_bytes = pickle.dumps(image_data) 
            delimeter_bytes = pickle.dumps(Config.delimeter)

            compressed_image_bytes = Helper.compress(image_bytes)
            
            print('sending image with size {}'.format(len(compressed_image_bytes)))
            client_socket.sendall(compressed_image_bytes + delimeter_bytes)
except Exception as e:
    print(traceback.format_exception())

server.close_connection()