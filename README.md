Написать клиент-серверное приложение, позволяющее клиенту скомпилировать .c файлы на сервере.
Клиент и сервер должны быть написаны на Python с использованием TCP сокетов.

Сервер слушает на заданном порту (по умолчанию порт 1234, можно задать при запуске через опцию -p)
и принимает запросы от клиентов (в бесконечном цикле). Клиенту можно передать адрес и порт сервера
(по умолчанию 127.0.0.1 1234, контролируется опциями -d и -p), а также путь к файлу. Клиент должен
послать серверу данный файл, перед файлом идет заголовок вида "File <filename>\n" (filename - имя файла).
Сервер должен скомпилировать файл компилятором Си и в ответ послать вердикт компиляции (Result: OK/Fail),
если Fail - лог с ошибками.

Добавьте возможность компилировать несколько файлов.
Клиенту передаются пути к файлам. Клиент посылает серверу эти файлы с заголовком "Number: <number of files>\n".
Далее следуют сами файлы, у каждого заголовок "File <filename>\n".

Добавьте возможность дополнительно передавать Makefile.
У клиента опция -m <путь к файлу>, при передаче клиент использует заголовок "Makefile: <filename>\n".
В таком случае сервер должен использовать make с этим Makefile.

Добавьте возможность удаленного обновления сервера на лету.
Опция для клиента -u, клиент добавляет в начало заголовок "Upgrade\n" и далее файлы как обычно
(количество, сами файлы, makefile если задан).
Сервер должен как обычно скомпилировать, и если все удачно - то заменить свой процесс на новую версию.
Если компиляция не удалась, то послать в ответ клиенту ошибку.

Добавите в сервер обработку сигнала SIGUSR1.
При получении данного сигнала сервер должен прервать все соединения, после чего продолжить работу.
Для отладки можно запустить клиент с большим файлом и послать сигнал серверу во время передачи.