import os
import socket

ip = socket.gethostbyname(socket.gethostname())
port = 1234


def compile_one_file(conn, request):
    # "File <filename>\n" (filename - имя файла).
    # Сервер должен скомпилировать файл компилятором Си
    # и в ответ послать вердикт компиляции (Result: OK/Fail),
    from_client = 'results.c'
    file_info = request.decode().split('\n')
    file_name_for_compilation = None

    with open(from_client, 'w') as file:
        for ind, string in enumerate(file_info):
            if string.startswith('File'):
                file_name_for_compilation = string.split(' ')[1].split('.')[0]
            else:
                file.write(string)

    # gcc <имя файла> -o <имя исполняемого файла>
    if file_name_for_compilation:
        new_file_name = file_name_for_compilation + '_compiled.exe'
        print(f'gcc {from_client} -o {new_file_name}')
        try_compile = os.system(f'gcc {from_client} -o {new_file_name}')
        if try_compile == 0:
            conn.sendall('Result: OK'.encode())
            print('Ok')
        else:
            conn.sendall('Result: Fail'.encode())
            print('Fail')
    os.remove(from_client)
    return 'compile_one_file'


if __name__ == "__main__":
    with socket.create_server((ip, port)) as server:
        while True:
            connection, addr = server.accept()
            print('connected:', addr)

            while True:
                # получаем байтовые строки
                request_file = connection.recv(1024*1024*1024)

                if not request_file or request_file == b'':
                    break

                if request_file.decode().startswith('File '):  # File <filename>\n" (filename - имя файла)
                    res = compile_one_file(connection, request_file)
                elif request_file.decode().startswith('Number:'):  # Number: <number of files>\n
                    pass
                elif request_file.decode().startswith('Makefile: \n'):  # Makefile: \n
                    pass
                elif request_file.decode().startswith('Upgrade\n'):  # Upgrade\n
                    pass

            connection.close()

