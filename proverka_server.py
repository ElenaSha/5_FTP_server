import socket
import os
import shutil #операции над файлами и директориями
import subprocess # работа с процессами, позволяет вызвать др. прогу. Например, функция subprocess.call("название проги") Можно передавать аргументы в списке
import threading

def ask(conn,addr):
	print(addr[0])
	msg = ''
	while True:
		data = conn.recv(1024)
		print("Получил инфу")
		return data


sock = socket.socket()
port = 1024

while True:
	try:
		sock.bind(('',port))
		break
	except:
			port+=1

print("Порт №", port)

sock.listen(1)
print("Ау")

while True:
	conn, addr = sock.accept()
	print("Поймал клиента")
	print(addr[0])
	client_thr = threading.Thread(target = ask, args=[conn,addr]).start()
	print("Поток создан")

sock.close()
