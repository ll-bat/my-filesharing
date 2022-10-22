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
            image_bytes = screenshot_helper.get_screenshot()
            to_send_bytes = Helper.get_to_send_bytes(image_bytes)
            
            print('sending image with size {}'.format(len(to_send_bytes)))
            client_socket.sendall(to_send_bytes)
except Exception as e:
    print(e)

server.close_connection()