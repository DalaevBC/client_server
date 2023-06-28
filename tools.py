import os


def compile_make_one_file(conn, request, make):
    """
    В функцию отдается запрос, затем происходит сортировка на make or file
    Фиксируем полеченный файл в "from_client" и выполняем через os.system
    """
    from_client = 'results.c'
    if make:
        #   Исхожу из того что на сервере уже есть файлы и мы получаем
        # только makefile и наша задача триггернуть его
        from_client = 'Makefile'
    file_info = request.decode().split('\n')
    file_name_for_compilation = None

    with open(from_client, 'w') as file:
        for ind, string in enumerate(file_info):
            if string.startswith('File') or string.startswith('Makefile'):
                file_name_for_compilation = string.split(' ')[1].split('.')[0]
            else:
                file.write(string)

    if file_name_for_compilation:
        try_compile = 1
        if make:
            try_compile = os.system(f'make')
        else:
            new_file_name = file_name_for_compilation + '_compiled.exe'
            try_compile = os.system(f'gcc {from_client} -o {new_file_name}')

        if try_compile == 0:
            conn.sendall('Result: OK'.encode())
            print('Ok')
        else:
            conn.sendall('Result: Fail'.encode())
            print('Fail')
    os.remove(from_client)
    return 'compile'


def compile_few_files(conn, request):
    file_info = request.decode().split('\n')
    all_file_dict = dict()

    for ind, string in enumerate(file_info):
        if string.startswith('File'):
            file_name_for_compilation = string.split(' ')[1].split('.')[0]
            new_file_name = file_name_for_compilation + '.c'
            all_file_dict[new_file_name] = file_info[ind+1]

    try_compile_result = 0

    for file_name, content in all_file_dict.items():
        with open(file_name, 'w') as file:
            file.write(content)

        new_file_name = file_name.replace('.c', '') + '_compiled.exe'
        try_compile = os.system(f'gcc {file_name} -o {new_file_name}')

        if try_compile != 0:
            try_compile_result = 1

        os.remove(file_name)

    if try_compile_result == 0:
        conn.sendall('Result: OK'.encode())
        print('Ok')
    else:
        conn.sendall('Result: Fail'.encode())
        print('Fail')

    return 'compile'


def sort_requests(connect):
    while True:
        request_file = connect.recv(1024 * 1024 * 1024)
        if not request_file or request_file == b'':
            break
        make = None
        if request_file.decode().startswith('File '):  # File <filename>\n"
            make = False
        elif request_file.decode().startswith('Makefile '):  # Makefile: \n
            make = True

        if make is None:  # Number: <number of files>\n
            res = compile_few_files(connect, request_file)
        else:
            res = compile_make_one_file(connect, request_file, make)

    return True


# *************  Для отправки, раскоментить и создать соответствующие файлы для отправки
# import socket

# IP = socket.gethostbyname(socket.gethostname())  # '127.0.0.1'
# PORT = 1234
#
#
# def send_file(ip, port, make, file_name):
#     sock = socket.socket()
#     sock.connect((ip, port))
#     send_type = 'File'
#     with open(file_name, "rb") as file:
#         file_data = file.read()
#         if make:
#             send_type = 'Makefile'
#         sock.send((bytes(f'{send_type} {file_name}\n', encoding='UTF-8')))
#         sock.sendall(file_data)
#         response = sock.recv(1024).decode()
#         print('response', response)  # Result: OK
#     sock.close()
#
#
# def send_few_files(ip, port):
#     sock = socket.socket()
#     sock.connect((ip, port))
#     sock.send((bytes(f'Number 3\n', encoding='UTF-8')))
#     send_type = 'File'
#     for file_name in file_names:
#         with open(file_name, "rb") as file:
#             file_data = file.read()
#             sock.send((bytes(f'{send_type} {file_name}\n', encoding='UTF-8')))
#             sock.sendall(file_data)
#             response = sock.recv(1024).decode()
#     print('response', response)  # Result: OK
#     sock.close()


# file_names = ['just_file.txt', 'just_file1.txt', 'just_file2.txt', 'just_file3.txt']
# send_file(IP, PORT, True, file_name='Makefile')
# send_file(IP, PORT, True, file_name='just_file.txt')
# send_few_files(IP, PORT)


