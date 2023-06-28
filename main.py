import socket
from tools import sort_requests

IP = socket.gethostbyname(socket.gethostname())
PORT = 1234

if __name__ == "__main__":
    with socket.create_server((IP, PORT)) as server:
        while True:
            connection, addr = server.accept()
            print('connected:', addr)
            result = sort_requests(connection)
            connection.close()
