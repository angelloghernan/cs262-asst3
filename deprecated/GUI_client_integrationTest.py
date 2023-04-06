import socket
import threading
from tkinter import *
# from chat import *

PORT = 65432
# server = "127.0.1.1"
# server = "134.209.220.140"
# Albert IP: 10.250.35.148
server = "10.250.35.148"
# server = "10.29.38.26"
address = (server, PORT)
format = "utf-8"

# Create a new socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)


# GUI class for the chat
class Client:
	# constructor method
	def __init__(self):
		self.test_result = []
		self.test_message = [
        "AUTOMATIC INTEGRATION TESTING BEGINS",
        "LENGTH TEST-THIS IS TO TEST IF THE APPLICATION CAN HANDLE ULTRA LONG MESSAGES OF UNREASONABLE LENGTH-TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2",
        "CR:Dean",
        "Hello Dean",
        "CR:",
        "This is a global message",
        "Hello Dean",
        "CR:",
		":::",
		"CR:UNITTEST",
		"      ",
        "TEST COMPLETE"
		]
		self.count = -1
		self.Window = Tk()
		self.Window.withdraw()

		# Notice that login will never fail
		# Repetitive user name only invalidate the previous session
		self.login = Toplevel()
		self.login.title("CS262 Chat application by Dean")
		self.login.resizable(width=True, height=True)
		self.login.configure(width=600,height=400)
		self.pls = Label(self.login,text="Please login to continue",
						justify=CENTER, font="Helvetica 16")

		self.pls.place(relheight=0.15,
					relx=0.2,
					rely=0.07)
		self.labelName = Label(self.login,
							text="Name and password: ",
							font="Helvetica 14")			
		self.labelName.place(relheight=0.2,
							relx=0.1,
							rely=0.2)

		# Create the entry box for the message
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

		# set the focus of the cursor
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

	# Activate the message page after login
	def goAhead(self, name):
		self.login.destroy()
		self.name = name
		self.expected_result = [
        self.name + ": " + "AUTOMATIC INTEGRATION TESTING BEGINS",
        self.name + ": " + "LENGTH TEST-THIS IS TO TEST IF THE APPLICATION CAN HANDLE ULTRA LONG MESSAGES OF UNREASONABLE LENGTH-TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2TEST_MESSAGE2",
        "The user you are trying to reach doesn't exist",
        "The user you are trying to reach doesn't exist",
        self.name + ": " + "CR:",
        self.name + ": " + "This is a global message",
        self.name + ": " + "Hello Dean",
        self.name + ": " + "CR:",
		self.name + ": " + ":::",
		self.name + ": " + "CR:UNITTEST",
		self.name + ": " + "      ",
        self.name + ": " + "TEST COMPLETE"
		]
		self.layout(name)
		# the thread to receive messages
		receive_thread = threading.Thread(target=self.receive)
		receive_thread.start()

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

		# create a scroll bar
		scrollbar = Scrollbar(self.textCons)

		# place the scroll bar
		# into the gui window
		scrollbar.place(relheight=1,
						relx=0.974)

		scrollbar.config(command=self.textCons.yview)

		self.textCons.config(state=DISABLED)

	# start the messaging thread
	def start_messaging_thread(self, msg):
		self.count = self.count + 1
		self.textCons.config(state=DISABLED)
		self.msg = msg
		self.entryMsg.delete(0, END)
		snd = threading.Thread(target=self.send_message)
		snd.start()

	# function to receive messages
	def receive(self):
		while True:
			try:
				message = client.recv(1024).decode(format)

				# if the messages from the server is NAME send the client's name
				if message == 'NAME':
					client.send(self.name.encode(format))
				elif message == 'GODIE':
					client.close()
				else:
					self.test_result.append(message)
					# if(self.test_result[self.count] == self.expected_result):
					# 	self.textCons.insert(END,"TEST" + self.count + "Passed\n\n")
					# print("This is test number" + self.count)
					# print("result[self.count] is:" + self.test_result[self.count])
					# print("self.expected_result is:" + self.expected_result)
					# print(self.test_result[self.count] == self.expected_result)
					# insert messages to text box
					self.textCons.config(state=NORMAL)
					if (message == self.expected_result[self.count-1]):
						self.textCons.insert(END, message + "\n\n" + "TEST PASSED" + "\n\n")
					else:
						self.textCons.insert(END, message + "\n\n")
					self.textCons.config(state=DISABLED)
					self.textCons.see(END)
			except KeyboardInterrupt:
				# an error will be printed on the command line or console if there's an error
				client.send("DIE".encode(format))
			except Exception:
				print("An error occurred!")
				client.close()
				break

	# function to send messages
	def send_message(self):
		self.textCons.config(state=DISABLED)
		print(self.count)
		msg = self.test_message[self.count]
		self.entryMsg.insert(0, msg)
		while True:
			message = (f"{self.name}: {self.msg}")
			client.send(message.encode(format))
			break


# create a GUI class object
g = Client()
print(g.test_result)