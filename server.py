import socket
import select
import sys

from _thread import *



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()

IP_address = str(sys.argv[1])

Port = int(sys.argv[2])

server.bind((IP_address, Port))

server.listen(100)

list_of_clients = []



def clientthread(conn, addr):
	"""
	sends a message to the client whose user object is conn
	"""
	conn.send(("Welcome!").encode('utf-8'))

	while True:
		try:
			message = conn.recv(2048)
			if message:
				print("<" + addr[0] + ">" + message)

				#Calls broadcast func to send message to all
				message_to_send = "<" + addr[0] + ">" + message
				broadcast(message_to_send, conn)
			else:
				#message may not have no content if the connection is broken
				remove(conn)
		except:
			continue


def broadcast(message, connection):
	"""
	broadcasts the message to all clients who's object
	is not the same as connection
	"""
	for clients in list_of_clients:
		if clients != connection:
			try:
				clients.send(message)
			except:
				clients.close()
				remove(clients)


def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)



while True:
	conn, addr = server.accept()

	list_of_clients.append(conn)

	print(addr[0] + " connected")

	#creates an individual thread for every user
	#that connects
	start_new_thread(clientthread, (conn,addr))

conn.close()
server.close()