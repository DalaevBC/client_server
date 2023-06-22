import socket

ip = socket.gethostbyname(socket.gethostname())  # '127.0.0.1'
port = 1234

# запрашиваем имя файла и отправляем серверу
file_name = 'just_file.txt'

# создаём сокет для подключения
sock = socket.socket()
sock.connect((ip, port))

with open(file_name, "rb") as file:
    file_data = file.read()
    sock.send((bytes(f'File {file_name}\n', encoding='UTF-8')))
    sock.sendall(file_data)
    response = sock.recv(1024).decode()
    print(response)  # Result: OK

sock.close()



