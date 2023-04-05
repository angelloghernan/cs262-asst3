import socket
import threading
import pickle
import tempfile
import os
import time
import calendar
# SSH root@134.209.220.140
# Password: HFY82305791HFY
# ufw allow 65432 in cloud server
# ufw allowimport socket
# HOST = "134.209.220.140"

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
ip_address = None

servers = []

# not persistent, do not save
server_sockets = []
server_name = ""

last_written_timestamp = None

# Testing
# name_message_map.update({"Huang":["This is the buffer message from before for Huang\n","Yes please"]})
# name_message_map.update({"Xie":["This is the buffer message for Xie\n","I love myself"]})

def get_timestamp():
    gmt = time.gmtime()
    return calendar.timegm(gmt)

def package_data():
    timestamp = get_timestamp()
    return [names, conn_name_map, name_conn_map, name_message_map, 
            name_loggedin, ip_address, servers, timestamp]

def unpackage_data(db, update_servers=False):
    global names
    global conn_name_map
    global name_conn_map
    global name_message_map
    global name_loggedin
    global ip_address
    global servers
    global last_written_timestamp
    names = db[0]
    conn_name_map = db[1]
    name_conn_map = db[2]
    name_message_map = db[3]
    name_loggedin = db[4]
    if update_servers:
        ip_address = db[5]
        servers = db[6]
    last_written_timestamp = db[7]


def updateDatabase(updateTimestamp=True):
    global last_written_timestamp
    saved_data = package_data()

    if not updateTimestamp:
        saved_data[7] = last_written_timestamp

    print(saved_data)
    # Update the db atomically
    with tempfile.NamedTemporaryFile(prefix=server_name, mode='wb', delete=False) as temp:
        pickle.dump(saved_data, temp)
        temp.flush()
        os.replace(temp.name, f"files/serverdb{server_name}.pickle")
        print("Updated database")
        if updateTimestamp:
            last_written_timestamp = saved_data[7]

def loadDatabase():
    try:
        with open(f"files/serverdb{server_name}.pickle", "rb") as database_file:
            db = pickle.load(database_file)
            print("loaded: ", db)
            unpackage_data(db, update_servers=True)
    except Exception as e:
        print("could not load database: ", str(e))
        pass

# Start the connection
def runServer(SERVER: str, server_socket: socket.socket):
    print("server is working on IP " + SERVER)
    server_socket.listen()

    while True:
        # Everytime it accepts creates a new socket to handle the connection
        conn, addr = server.accept()

        print("Accepting connection from client")
        
        conn.send("NAME".encode(FORMAT)) # Ask the client: what is your name?

        # 1024 represents the max amount
        # of data that can be received (bytes)
        name = conn.recv(1024).decode(FORMAT)

        # Process and update all informations
        names.append(name)
        conn_name_map.update({conn:name})
        name_conn_map.update({name:conn})
        name_loggedin.update({name:1})
        updateDatabase()

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
def serve_client(conn: socket.socket, addr):
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
                print("sender name is", sender_name)
                print("recipient name is:", recipient_name)

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

    # The client is GONE
    # Clear elements from the double maps
    del conn_name_map[conn]
    for n,c in name_conn_map.copy().items():
        if(c==conn):
            del name_conn_map[n]
    print("conn is close and the name_conn_map is",name_conn_map)
    name_loggedin.update({sender_name:0})
    updateDatabase()
    # Close the connection and beware that the socket cannot be reused
    conn.send("GODIE".encode(FORMAT))
    conn.close()
    # We don't really have to return but this is for extended unit test concerns
    # return "serve_client_CLOSED"

# method for broadcasting
# messages to the each clients / specific client

def broadcastMessageAll(message):
    for conn in name_conn_map.copy().values():
        try:
            conn.send(message)
            print("message sent to", conn_name_map[conn])
        except BrokenPipeError:
            pass
        except IOError as e:
            print(str(e) + "gracefully shutted down")
            

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
                    updateDatabase()
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

# Receive pickled data format first by reading the length of the pickled data
# and then by reading the amount of bytes in the message
def receive_pickled_data(sock: socket.socket):
    received_data = b''
    size = int(sock.recv(4096).decode(FORMAT))
    while len(received_data) < size:
        received_data += sock.recv(4096)
    return pickle.loads(received_data)

# Send pickled data format first by sending the length of the pickled data
# and then by reading the amount of bytes in the message
def send_pickled_data(sock: socket.socket):
    data = package_data()
    serialized_data = pickle.dumps(data)
    sock.send(str(len(serialized_data)).encode(FORMAT))
    sock.sendall(serialized_data)
    sock.send("FINISH".encode(FORMAT))

def server_listen(address: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    sock.bind((address, port))
    while True:
        try:
            sock.listen()
            conn, _ = sock.accept()
            # First message: timestamp, sent by other end
            timestamp = int(conn.recv(1024).decode(FORMAT))
            print("Timestamp received: ", timestamp)
            if last_written_timestamp is None or timestamp > last_written_timestamp:
                print("Updating database...")
                conn.send("REQUEST".encode(FORMAT))
                conn.recv(4096) # wait for ack
                print("Updating database...")
                data = receive_pickled_data(conn)
                unpackage_data(data)
                print("Updating database...")
                updateDatabase()
                conn.send("OK".encode(FORMAT))
            elif timestamp < last_written_timestamp:
                print("Sending information...")
                conn.send("SENDING".encode(FORMAT))
                print("Sending information...")
                conn.recv(4096) # wait for ack
                print("Sending information...")
                send_pickled_data(conn)
                conn.recv(4096) # get ack
            while True:
                try:
                    time.sleep(2)
                    print("Listening for heartbeat...")
                    hb = conn.recv(4096).decode(FORMAT)
                    if not hb == "HEARTBEAT":
                        print("Lost connection with another server")
                        break
                    print("Heart beat received: ", hb)
                except:
                    print("Lost connection with another server")
                    break
        except Exception as e:
            print("Error listening to another server: ", str(e))

def server_connect(address: str, port: int) -> None:
    sock = None
    while True:
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
            print("Trying to connect to server")
            sock.connect((address, port))
            print("Connection established")
            sock.send(str(last_written_timestamp).encode(FORMAT))
            response = sock.recv(4096).decode(FORMAT)
            print("Response received: ", response)
            sock.send("ACK".encode(FORMAT))
            print("Sent ACK")
            if response == "REQUEST":
                print("Sending information...")
                send_pickled_data(sock)
                sock.recv(4096) # get ack
            else:
                print("Receiving information...")
                data = receive_pickled_data(sock)
                unpackage_data(data)
                updateDatabase()
                print("Sending ACK (OK)")
                sock.send("OK".encode(FORMAT))
            while True:
                try:
                    time.sleep(2)
                    print("Sending heartbeat...")
                    sock.send("HEARTBEAT".encode(FORMAT))
                except:
                    print("Lost connection with another server")
                    sock.close()
                    break
        except Exception as e:
            print(str(e))
            print(f"Connection failed for {address}:{port}, trying again in 3 seconds")
            if sock:
                sock.close()
            time.sleep(3)


if __name__ == "__main__":
    server_name = input("What is this server's name/identity?: ")

    loadDatabase()
    PORT = 65432
    SERVER = None
    updated = False

    if ip_address == None:
        SERVER = input("Please enter the IP to start this server on: ")
        ip_address = SERVER
        updated = True
    else:
        SERVER = input("Please enter the IP to start this server on, or type nothing to use the previous IP: ")
        if SERVER == "":
            SERVER = ip_address

    print(f"The following servers and ports are on record: {servers}")

    while True:
        other_address = input("Please enter the IP of another existing server, or type nothing to stop: ")
        if other_address == "":
            break
        other_port = input("Please enter the port this connection will use: ")
        other_port = int(other_port)

        should_connect = input("Should this server connect to this address (instead of listening for it)?: [Y/n]")
        should_connect = should_connect != "n" and should_connect != "N"

        servers.append((other_address, other_port, should_connect))

    for (i, (address, port, should_connect)) in enumerate(servers):
        if should_connect:
            thread = threading.Thread(target=server_connect, args=(address, port))
            thread.start()
        else:
            thread = threading.Thread(target=server_listen, args=(ip_address, port))
            thread.start()

    ADDRESS = (SERVER, PORT)
    # Create a socket that accepts connection
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    server.bind(ADDRESS)
    ip_address = SERVER
    updateDatabase(updateTimestamp=False)
    runServer(SERVER, server)
