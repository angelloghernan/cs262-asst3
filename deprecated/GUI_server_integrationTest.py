import socket
import threading
# ufw allow 65432 in cloud server
# ufw allowimport socket
# HOST = "134.209.220.140"

# Choose a port that is free
PORT = 8000
# An IPv4 address is obtained for the server.
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '127.0.0.1'
# Address is stored as a tuple
ADDRESS = (SERVER, PORT)
# the format in which encoding and decoding will occur
FORMAT = "utf-8"

# Dynamically allocated arrays and dictionarys
# Can be changed into using database
names = []
# Bi-directional mapping between socket and name 
# Different client serving threads can access the global information
conn_name_map = dict()
name_conn_map = dict()

# Message buffer for not logged-in but registeredusers
name_message_map = dict() # A map from a username to a list of messages
# keep track of registered users and their state of connectedness
name_loggedin = dict()

# Testing messages
# name_message_map.update({"Huang":["This is the buffer message from before for Huang\n","Yes please"]})
# name_message_map.update({"Xie":["This is the buffer message for Xie\n","I love myself"]})

server=socket.socket(socket.AF_INET,
					socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the address of the server to the socket
server.bind(ADDRESS)

# function to start the connection


def runServer():

	print("server is working on " + SERVER)

	# listening for connections
	server.listen()

	while True:

		# accept connections and returns
		# a new connection to the client
		# and the address bound to it
		conn, addr = server.accept()
		
		conn.send("NAME".encode(FORMAT)) # Ask the client: what is your name?

		# 1024 represents the max amount
		# of data that can be received (bytes)
		name = conn.recv(1024).decode(FORMAT)

		# Process and update all informations
		names.append(name)
		conn_name_map.update({conn:name})
		name_conn_map.update({name:conn})
		name_loggedin.update({name:1})

		# Debugging message, or show list if desired on the server's end
		# print(conn_name_map)
		# print(name_conn_map)
		# print(f"Name is :{name}")
		# print(f"Conn is :{conn}")

		# broadcast message
		print("the chat has just begun and the name_conn_map is",name_conn_map)
		# broadcastMessageAll(f"{name} has joined the chat!".encode(FORMAT))

		conn.send('Connection successful!\n\n'.encode(FORMAT))

		exhaust_name_message_map(name,conn)

		# Start the handling thread
		thread = threading.Thread(target=serve_client,
								args=(conn, addr))
		thread.start()
		# This is to print out the number of clients online and also for debugging such as broken pipe error and bad fiel descriptor
		print(f"number of connections is {threading.activeCount()-1}")

# receive incoming messages and send to specified recipients
def serve_client(conn, addr):
	print(f"NEW CONNECTION {addr}")
	connected = True
	sender_name = conn_name_map[conn]
	recipient_name = ""

	while connected:
		# receive message
		try:
			message = conn.recv(1024)
			decoded_message = message.decode(FORMAT)
			if(decoded_message):
				print("decoded message is", decoded_message)

			# exhaust_name_message_map(sender_name,conn)

			# All the processing that happen within before broadcasted out!
			if (decoded_message.startswith(sender_name + ": " + "CR:") or decoded_message.startswith(sender_name + ": " + "RE:")):
				recipient_name = decoded_message[5+len(sender_name):].strip()
				print("recipient name changed to:", recipient_name)
			
			if (decoded_message.startswith(sender_name + ": " + "EXIT")):
				name_loggedin[sender_name] = 0
				conn.send("LOG OUT SUCCESSFUL, PLEASE CLOSE THE WINDOW".encode(FORMAT))
				print("name_loggedin is", name_loggedin)
				break
			if (decoded_message.startswith(sender_name + ": " + "DELETE_EXIT")):
				del name_loggedin[sender_name]
				names.remove(sender_name)
				conn.send("ACCOUNT DELETION IS SUCCESSFUL, PLEASE CLOSE THE WINDOW".encode(FORMAT))
				print("name_loggedin is", name_loggedin)
				print("names is", names)
				break

			if (decoded_message.startswith(sender_name + ": " + "LIST_USERS")):
				result = "The list of users currently registered are:"
				for str in names:
					result = "\n" + result + str + "\n"
				conn.send(result.encode(FORMAT))

			# broadcast message
			if(recipient_name == ""):
				broadcastMessageAll(message)
			else:
				# broadcastMessageAll(message)
				broadcastMessageFromTo(sender_name,message,recipient_name)
		except BrokenPipeError:
			connected = False
		except KeyboardInterrupt:
			connected = False

	# The client is DEAD
	# Clear elements from the double maps
	del conn_name_map[conn]
	for n,c in name_conn_map.copy().items():
		if(c==conn):
			del name_conn_map[n]
	print("conn is close and the name_conn_map is",name_conn_map)
	name_loggedin.update({sender_name:0})
	# Close the connection and beware that the socket cannot be reused
	conn.send("GODIE".encode(FORMAT))
	conn.close()
	# We don't really have to return but this is for extended unit test concerns
	return "serve_client_CLOSED"

# method for broadcasting
# messages to the each clients / specific client

def broadcastMessageAll(message):
	for conn in name_conn_map.values():
		try:
			conn.send(message)
		except BrokenPipeError:
			print("Brokenpipe handled")
		except IOError as e:
			print("e" + "gracefully shutted down")
			

def broadcastMessageFromTo(sender,message,name):
	decoded_message = message.decode(FORMAT)
	if(decoded_message != ''): # We don't allow empty message
		if(name in name_loggedin.keys() and name in names): # If the name has appeared before
			if(name_loggedin[name] == 1): # If the user is logged in
				name_conn_map[name].send(message) # Then just directly send the message
			else:
				if(name not in name_message_map.keys()):
					# Create a new mapping
					print("name not in name_message_map")
					message_list = ["\n Below is the list of unread messages\n"]
					message_list.append(message.decode(FORMAT))
					name_message_map.update({name:message_list})
					print("successfully added to ", name)
					return "successfully added to " + name
				elif(name in name_message_map.keys()):
					print("name in name_message_map")
					message_list = name_message_map[name]
					message_list.append("\n" + message.decode(FORMAT)+"\n")
					name_message_map[name] = message_list
			name_conn_map[sender].send(message)
			print("message buffer:",name_message_map)
		else: # We are trying to message someone who doesn't exist
			non_existence_message = "The user you are trying to reach doesn't exist"
			name_conn_map[sender].send(non_existence_message.encode(FORMAT))
			return non_existence_message

# Send all the corresponding message from the buffer when a registered user log in
def exhaust_name_message_map(name, conn): # Conn is the socket
	if(name in name_message_map.keys()):
		print("exhaust_name_message_map: name in name_message_map.keys()")
		for decoded_message in name_message_map[name]:
			print("message sent from the message buffer")
			try:
				conn.send(decoded_message.encode(FORMAT))
			except BrokenPipeError:
				break


# call the method to
# begin the communication
runServer()
