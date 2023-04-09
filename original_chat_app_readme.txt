This is from the first design project. Some parts of this may now be slightly outdated, but the information on how to perform the chat features like creating accounts and listing accounts, etc., is still relevant. Look at the "Feature" sections here for more information. Please read `README.md` for more information too.

I employed LAMP server (droplet) that suffices to support such a light-volume application
Server-side setup instruction: 
	Cloud Server (Suggested):
	Log into the cloud server
	Type ufw allow {port number want to listen on}
	Run python3 GUI_chat_server.py
	Local: Run python3 GUI_chat_server.py 
Client side setup instruction: Run python3 GUI_chat_client.py
Adapt the address and port number accordingly inside the program.

Feature 1: Create an account. 
Operation: on the log-in interface, type in the username to register or log in.
All user names are indeed uniquely store in the back-end; name is the unique identifier of operations in the application (such as unread message and direct message)
If input collides with existing username, automatically log in as the username
If input collides with existing username and the user is already logged in, automatically log in as the username and invalidate the previous machine logged in as the name.
If input is unseen before, create an account associated with that name

Feature 2: List accounts
Operation: on users’ text bar: Type in “LIST_USERS” prints out all registered users in the application

Feature 3: “Recipient Name”: Send a message to all recipients (global chat room)
1, By default, recipient is global; or, in order to change back to global, type in “CR:”
2, Type in messages want to send in the text bar;
Explanation: All logged in users will be able to receive the message; Global chat room messages will not be included in message buffers, aka, unlogged in users will not receive them even after they log in

Feature 4: “Recipient Name”: Send a message to a recipient (direct, private message)
1, In order to change to private chat with a specified recipient, type in “CR:” + the username you want to reach
2, If the user doesn’t exist, an error message will occur;

Feature 5: Send unsent messages
Messages sent to registered but not logged-in users will be stored inside the message buffer; the buffer will be automatically depleted after the user log in
The message buffer will not hold anything for not registered usernames

Feature 6: Delete an account
Operation: Type in “DELETE_EXIT” in the text bar
The account record will be wiped from the server, but other clients can still register as the same name afterwards, aka, reuse the same name

Feature 7: Close the application:
Operation: Type in “EXIT” in the text bar, and  then simply close the window and press Ctrl+C in the terminal.


Reference

1.	http://web.mit.edu/6.102/www/sp23/classes/02-testing/#automated_unit_testing
2.	https://medium.com/@mashood.snhu/automated-unit-testing-of-a-web-application-in-python-de426afda5a3
3.	https://stackoverflow.com/questions/15958026/getting-errno-9-bad-file-descriptor-in-python-socket/15958099#15958099
4.	https://github.com/erdc/python/blob/master/Lib/test/test_socket.py
5.	https://stackoverflow.com/questions/40814712/python-connectionrefusederror-errno-61-connection-refused
6.	https://realpython.com/python-sockets/#conclusion
7.	https://stackoverflow.com/questions/36060346/creating-a-simple-chat-application-in-python-sockets
8.	https://9to5answer.com/socket-error-errno-32-broken-pipe
9.	https://stackoverflow.com/questions/36366774/python-peer-to-peer-chat-sockets
10.	https://stackoverflow.com/questions/27913310/how-to-get-the-content-of-a-tkinter-text-object
11.	https://github.com/MelleDijkstra/python-grpc-chat
12.	https://github.com/ryan95f/python-grpc-chat-app
13.	GitHub - Madhur215/Django-ChatApp: A chat application built using Django Rest Framework. Users can add other users as friends and have one to one chat.
14.	https://stackoverflow.com/questions/48121620/python-unittest-multiple-tests-on-tcp-server-with-single-socket
15.	https://pythonguides.com/python-exit-command/

I affirm my awareness of the standards of the Harvard College Honor Code. While completing this homework, I have worked through the project shown here myself, in line with the academic integrity policy of the class. The work submitted represents my own knowledge and solution of the core/majority of specs in the assignment requirement. I hereby declare that this project is finished with reference to the above sources, including but not limited to:
	referencing the partial design/structure of code within the reasonable range;
	referencing library usage and a particular combination of python libraries
	referencing function API design
	following wire protocol design mind-map
