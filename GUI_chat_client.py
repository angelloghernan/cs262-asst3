import time
import socket
import threading
from typing import List
from tkinter import *
# FOR USER: change the server IP to the IP of the server you are using, and the port to the port you are using. By default PORT = 65432 should work. 
PORT = 65432
server = "localhost"
# Some information for our own reference:
# server = "127.0.1.1"
# server = "134.209.220.140"
# Albert IP: 10.250.35.148
# server = "10.250.35.148"
# server = "10.29.38.26"
address = (server, PORT)
format = "utf-8"

active_server = 0

# Some information for our own reference:
# Albert's Macbook's laptop IP: "10.250.35.148"
# Gianni's Laptop IP: "10.250.36.224"
servers = ["10.250.2.71", "10.250.36.224"] # FOR USER: change this for the demo and whatnot. should have 2 servers
servers = ["10.250.35.148"]
# servers = ["10.250.2.71", "10.250.35.148"] 
servers = ["10.250.44.100", "10.250.35.148"]
servers = ["10.250.35.148", "10.250.36.224"]
# servers = ["10.250.44.100"]
sockets: List[socket.socket] = []

for server in servers:
    address = (server, PORT)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(address)
    sockets.append(client)

# Create a new socket

# GUI class for the chat
class Client:
    # constructor method
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("CS262 Dean Login Page")
        self.login.resizable(width=False,
                            height=False)
        self.login.configure(width=400,
                            height=300)
        # create a Label
        self.pls = Label(self.login,
                        text="Please login to continue",
                        justify=CENTER,
                        font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                    relx=0.2,
                    rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                            text="Name and password: ",
                            font="Helvetica 12")
                            

        self.labelName.place(relheight=0.2,
                            relx=0.1,
                            rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                            font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                            relheight=0.12,
                            relx=0.38,
                            rely=0.2)
        
        self.password = Entry(self.login,
                            font="Helvetica 14")

        self.password.place(relwidth=0.4,
                            relheight=0.12,
                            relx=0.38,
                            rely=0.4)

        # Focus of cursor
        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                        text="Register if first time use/ Login",
                        font="Helvetica 14 bold",
                        command=lambda: self.goAhead(self.entryName.get()))
        self.go.config(cursor="sb_right_arrow")
        self.go.place(relx=0.2,
                    rely=0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.name = name
        self.layout(name)
        # the threads to receive messages
        for i, client in enumerate(sockets):
            receive_message_thread = threading.Thread(target=self.receive, args=(client, i))
            receive_message_thread.start()

    # The main layout of the chat
    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CS262")
        self.Window.resizable(width=True,
                            height=True)
        self.Window.configure(width=470,
                            height=550,
                            bg="orange")
        self.labelHead = Label(self.Window,
                            bg="#17202A",
                            fg="#EAECEE",
                            text=self.name,
                            font="Helvetica 13 bold",
                            pady=5)
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                        width=450,
                        bg="orange")
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
        self.textCons = Text(self.Window,
                            width=20,
                            height=2,
                            bg="blue",
                            fg="#EAECEE",
                            font="Helvetica 14",
                            padx=5,
                            pady=5)
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
        self.labelBottom = Label(self.Window,
                                bg="#ABB2B9",
                                height=80)
        self.labelBottom.place(relwidth=1,
                            rely=0.825)
        self.entryMsg = Entry(self.labelBottom,
                            bg="#2C3E50",
                            fg="#EAECEE",
                            font="Helvetica 13")

        # incorporate into the GUI
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
        self.entryMsg.focus()

        # Button used for sending messages
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.start_messaging_thread(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)
        self.textCons.config(cursor="star")
        self.buttonMsg.config(cursor="heart")
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

    # start the messaging thread
    def start_messaging_thread(self, msg):
        for client in sockets:
            self.textCons.config(state=DISABLED)
            self.msg = msg
            self.entryMsg.delete(0, END)
            send_message_thread = threading.Thread(target=self.send_message, args=[client])
            send_message_thread.start()
            print(threading.active_count())

    # function to receive messages
    def receive(self, client: socket.socket, server_no: int):
        global active_server
        while True:
            try:
                message = client.recv(1024).decode(format)
                # For debugging:
                print(message)
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(format))
                elif message == 'GODIE':
                    client.close()
                # if this isn't the active server we're listening to, then we ignore the message
                elif active_server == server_no:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message+"\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except KeyboardInterrupt:
                # an error will be printed on the command line or console if there's an error
                client.send("DIE".encode(format))
            except Exception as e:
                # if there's an error, we assume the server is down. Then, we switch servers to a working one, so that we are 2-fault tolerant in the face of crash/failstop failures.
                # naively round robin to the next server as the active server if this server is down
                if active_server == server_no:
                    active_server += 1
                    active_server %= len(servers)
                print(f"Error when communicating with server {server_no}, trying again in 5 seconds...")
                # For debugging:
                print(str(e))
                time.sleep(5)

    # function to send messages
    def send_message(self, client: socket.socket):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(format))
            # assumed that if a message fails, the server is dead,
            # will come back online and download the updated data from another server
            break


# create a GUI class object
g = Client()
