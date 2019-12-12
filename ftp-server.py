import socket
import os
import shutil #операции над файлами и директориями
import subprocess # работа с процессами, позволяет вызвать др. прогу. Например, функция subprocess.call("название проги") Можно передавать аргументы в списке
import threading
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
cat <filename> - отправляет содержимое файла
'''

dirname = os.path.join(os.getcwd(), 'docs')

def ask(conn,addr):
	print(addr[0])
	msg = ''
	while True:
		data = conn.recv(1024)
		print("Получил инфу")
		return data

def process(conn, addr):

	req = ask(conn,addr).decode()
	req_lst = req.split()

	#см директорию
	if req =='pwd':
		return dirname

	elif req == 'ls':
		return '; '.join(os.listdir(dirname))

	elif req_lst[0] == 'rm':
		subprocess.call(["rm", os.path.join(dirname, req_lst[1])])
		return "File deleted."

	elif req_lst[0] == 'cat':
		with open(os.path.join(dirname, req_lst[1]), 'r', encoding='UTF-8') as f:
			return f.read()

	#ДОДЕЛАТЬ
	elif req_lst[0] == 'cp1':
		conn.send('ready'.decode()) #special message to client to start receiving text
		subprocess.call(["touch", os.path.join(dirname, req_lst[1])])
		with open(os.path.join(dirname, req_lst[1]), 'w', encoding='UTF-8') as f:
			f.write(conn.recv())
		return 'Done.'

	#ДОДЕЛАТЬ НА КЛИЕНТЕ
	elif req_lst[0] == 'cp2':
		with open(os.path.join(dirname, req_lst[1]), 'r', encoding='UTF-8') as f:
			return f.read()

	elif req_lst[0] == 'mv':
		old = req_lst[1]
		new = req_lst[2]
		subprocess.call(["mv", os.path.join(dirname, old), os.path.join(dirname, new)])
		return 'File renamed.'

	elif req_lst[0] == 'mkdir':
		subprocess.call(["mkdir", os.path.join(dirname, req_lst[1])])
		return 'Direction made'

	elif req_lst[0] == 'rmdir':
		subprocess.call(["rmdir", os.path.join(dirname, req_lst[1])])
		return 'Direction deleted'

	elif req == 'exit': 	#8
		print("Что ж ты, фраер, сдал назад")
		conn.close()
		return 'exit'

	else:
		return 'bad request'


#while True:
    #conn, addr = sock.accept()
    
    
    #response = process(request) # какой к черту реквест
    #conn.send(response.encode())


# САМА ПРОГА

sock = socket.socket()
port = 6666

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
	#client_thr = threading.Thread(target = process, args=[conn,addr]).start()
	#print("Поток создан")
	responce = process(conn,addr)
	if responce == 'exit':
		break
	else:
		conn.send(responce.encode())

sock.close()
