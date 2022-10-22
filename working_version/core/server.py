import socket

class Server:
    host_ip = None 
    port = None 
    socket = None 

    def __init__(self, host_ip, port) -> None:
        self.host_ip = host_ip 
        self.port = port 
        self.create_socket()

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind_address(self):
        self.socket.bind((self.host_ip, self.port))

    def start_server(self):
        self.bind_address()
        print('server started at {}:{}'.format(self.host_ip, self.port))

    def connect(self):
        self.socket.connect((self.host_ip, self.port))

    def wait_for_connections(self, num_connections=1):
        self.socket.listen(num_connections)
        print('waiting for connection')

    def get_connection(self):
        return self.socket.accept() 

    def close_connection(self):
        self.socket.close()

    def receive_bytes(self, bytes_len=4 * 1024):
        return self.socket.recv(bytes_len)

    def __del__(self, *args, **kwargs):
        self.close_connection()
