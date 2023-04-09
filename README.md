This file also contains our Engineering Notebook, which is the last section. 

# Usage
## Chat features
The information from design project 1 on how to perform the chat features like creating accounts and listing accounts, etc., is found in `original_chat_app_readme.txt`. That information is not relevant to this specific design project 3, so we did not include it here.

## Running with just 1 server for the first time

Run `python GUI_chat_server_test_ver2.py` or `python3 GUI_chat_server_test_ver2.py` to start the server for the first time and follow the instructions on the terminal like this:

        % python GUI_chat_server_test_ver2.py 
        What is this server's name/identity?: [INSERT NAME]
        [THIS MESSAGE IS OKAY BECAUSE IT'S THE FIRST TIME RUNNING SERVER]
        could not load database:  [Errno 2] No such file or directory: 'files/serverdb[INSERT NAME].pickle'
        Please enter the IP to start this server on: [INSERT IP]
        The following servers and ports are on record: []
        Please enter the IP of another existing server, or type nothing to stop: [TYPE NOTHING AND HIT ENTER (since we're only using 1 server here)]
        [[], {}, {}, [INSERT IP], [], None]
        Updated database
        server is working on IP [INSERT IP]

For example, if you want to run the server "test1" on IP 10.250.35.148:

        % python GUI_chat_server_test_ver2.py
        What is this server's name/identity?: test1
        could not load database:  [Errno 2] No such file or directory: 'files/serverdbtest1.pickle'
        Please enter the IP to start this server on: for the first tim10.250.35.148
        The following servers and ports are on record: []
        Please enter the IP of another existing server, or type nothing to stop: 
        [[], {}, {}, '10.250.35.148', [], None]
        Updated database
        server is working on IP 10.250.35.148

## Running with just 1 server by re-starting previous server
This demonstrates how it can be stopped and re-started without losing messages that were sent during the time it was running. You just run `python GUI_chat_server_test_ver2.py` or `python3 GUI_chat_server_test_ver2.py` and use the same server name as before to re-start it.

For example, if you want to re-start the server "test1" on the same IP address: 

        % python GUI_chat_server_test_ver2.py
        What is this server's name/identity?: test1
        loaded:  [[], {}, {}, '10.250.35.148', [], None]
        Please enter the IP to start this server on, or type nothing to use the previous IP: 
        The following servers and ports are on record: []
        Please enter the IP of another existing server, or type nothing to stop: 
        [[], {}, {}, '10.250.35.148', [], None]
        Updated database
        server is working on IP 10.250.35.148

## Running with multiple servers


In all cases, press Ctrl+C in the terminal to shut the server down. To shut down the client, type in “EXIT” in the text bar, then simply close the window and press Ctrl+C in the terminal.


# About 
We fully implemented the specification on Canvas. We took the wire protocol implementation we created for the first design exercise (the chat application) and re-design it so that the system is both persistent (it can be stopped and re-started without losing messages that were sent during the time it was running) and 2-fault tolerant in the face of crash/failstop failures. We replicated the back end of the implementation and made the message store persistent. 

See "Engineering Notebook" section below for more details on the decision-making process and design.


# Testing
To run the unit tests, simply run the command

python FUNCTION_TO_BE_TESTED_unittest.py

For example:

        % python get_stamp_unittest.py                                                130 ↵ ✹
        .
        ----------------------------------------------------------------------
        Ran 1 test in 0.000s

        OK
    
There are four files to run the unit tests. The tests are conducted on presumed input spaces without much testing on non-benign/malicious inputs since our functions are embedded for use in parent functions. Waldo also said this is good. If desired, more test cases can be added simply by adding more test functions under the test class, though we already tested all the functionality needed for the specification.

More details on the tests are in "Engineering Notebook" section below.


# Engineering Notebook
# Day 1: 4-4
- We needed to pick whether to use the wire protocol or gRPC version of our 1st design project. We decided to use our wire protocol implementation for the 1st design project rather than the gPRC version because we felt like the wire protocol version was cleaner, simpler, and thus more convenient to work with. We also preferred relying less on external packages/libraries to handle this because that way we feel more confident about being able to build a distributed system like this from scratch.
- This day, we reviewed our wire protocol code for the 1st design project and reviewed sockets. We played around with some code for this. 
  - For example, we ran into a bug where the network and ports weren't working properly, and the bug turned out to be caused by our computers' firewall settings. We fixed this by turning off the firewall. 
- We reviewed the content from class related to this design project, including material related to persistence, replication, fault tolerance, and consensus. 
- We thought about how we would need to modify our implementation to have multiple servers to make it 2-fault tolerant. Previously, we had just 1 central server - to make it 2-fault tolerant, we would want to support 3 servers, so that if 2 of those servers failed, 1 server would still be running and useable. 
- We also brainstormed different ways to make the message store persistent. What kind of databases would we need? We planned on doing more research and thinking on this.
- We felt like we needed to sketch out exactly what it was we needed to do for the project (since some of the details weren't so clear), so we planned on asking questions to clarify the details.
  - For example, we weren't sure if we needed to implement a consensus algorithm or not. We decided to ask about this.
  - We also weren't sure if we had to handle re-joining a replica that has failed. We decided to ask about this.
  - Similarly, we had other questions about the details of the project, where we felt like there were easier ways to implement the project by strictly sticking to the specification, but we weren't sure that was okay (because some of those decisions might not be the best to use in practice, like at a real tech company). We decided to ask about this.

# Day 2: 4-6
- We asked the questions we had and got a ton of helpful feedback.
  - For example, we were learned that we did NOT have to implement a consensus algorithm. So, we decided NOT to implement a consensus algorithm because this way would be simpler and cleaner to implement, and we think this will reduce the chance of bugs occurring.
  - We learned that we did NOT have to handle re-joining a replica that has failed. So, we decided NOT to handle this because this way would be simpler simpler and cleaner to implement, and we think this will reduce the chance of bugs occurring.
  - We learned that we ONLY had to implement what was specifically mentioned in the specification. So, we decided to stick to the specification and not implement anything else that wasn't mentioned in the specification. This way would be simpler and cleaner to implement, and we think this will reduce the chance of bugs occurring.
- In particular, based on what we learned, we decided to achieve persistence by just storing all the information and data on the server in a pickle file. 
  - We used Python pickle, a module that allows you to serialize and deserialize Python objects. Serialization is the process of converting an object in memory to a byte stream that can be stored on disk, and this allows that Python object to be saved and restored in the future via deserialization (converting a byte stream back into a Python object).
  - We decided to pickle a list consisting of `[names, name_message_map, ip_address, servers, timestamp]` because those are all the relevant data structures we need to store to make the server persistent. Then, when we re-start the server, we just unpickle that list and restore the data structures to their previous state. We would name the pickle file after the server name so that we know which pickle file to unpickle when we re-start the server.
  - Using a pickle file is much simpler and cleaner to implement than using a more complex database like MySQL or Postgres, and we think this will reduce the chance of bugs occurring. So, we are happy to just use a simple pickling and unpickling solution because this still satisfies the specification.
- We then implemented the code for persistence in Python using the above strategy. We ran into some bugs with pickling and unpickling the files if the server was being run for the first (vs. not first) time, so we added some try-except clauses to check for each case and handle them separately. That fixed the bugs. 
  - We basically finished the persistence code for a single server this day. 

# Day 3: 4-8
- To implement the replication and 2-fault tolerance, we decided to have up to 3 servers running simultaneously, with every client sending every message to all servers, then all servers update their state based on the client's message, and then only 1 of those servers responds. We decided to use this model because it is simple and clean to implement, and we think this will reduce the chance of bugs occurring. Plus, this still satisfies the specification.
  - Intuitively, this achieves 2-fault tolerance because if 2 of the servers fail, then 1 server will still be running and useable. Then, since the clients are communicating with all the servers, the clients will essentially not notice that 2 of the servers failed. 
  - The servers have a designated leader, which is the server that responds to the client. The servers all send heartbeat messages between each other so every server knows the status of ever other server (whether the other server is offline or online). So, if the leader goes offline, then another server becomes the leader. So, there will always be 1 server that responds to the client, regardless of if up to 2 of the servers fail.
  - We recognize that this model is not the most efficient or scalable model, and that this model would likely not be used in real life at a big tech company because it is infeasible for all the clients to message all the servers, but we decided to go with this model because it is simple and clean to implement while it still satisfies the specification.
- We then implemented the code for replication and 2-fault tolerance in Python using the above strategy. We ran into some bugs with communication between the servers, but we fixed those by designating which server is listening vs actively connecting to each other. We also tested our code to make sure that it worked. 
- We also updated our code for persistence to make sure that the data structures were being updated correctly when the servers communicate with each other. Specifically, we would have a server update their pickled data to whatever data is the most recent, which is determined by the timestamps attached to messages sent. So, if server A gets a message from server B that is more recent (newer timestamp), then server A updates its database (which is its pickle file) to match server B's newer data. Thus, we are able to achieve both persistence, replication, and 2-fault tolerance.
- Project is officially finished, besides unit testing. We will do unit testing tomorrow.

# Day 4: 4-9
- We wrote the unit tests for our project. We used the Python `unittest` library to make sure that the functions are working as intended. We also ran our code as a whole to make sure that the entire program is working as intended.
- Instructions for how to run the unit tests are earlier in  the `Testing` section of this README.
- loadDatabase_unittest.py: This unit test checks whether the loadDatabase function correctly reads a pickled file and calls the unpackage_data function with the correct arguments. The unittest also checks if the loadDatabase function raises an exception when the pickled data is invalid (e.g., corrupted or not a pickled file), and checks if the loadDatabase function correctly reads a pickled file with a custom server name, and whether the pickle.load function is called.
- get_stamp_unittest.py: This unit test checks if the get_timestamp function returns the correct Unix timestamp (seconds since the epoch) value based on the current time in the UTC timezone. 
- send_pickled_data_and_package_data_unittest.py: This unit test checks if the send_pickled_data function sends the serialized data correctly over a socket connection. They use MagicMock instances for sockets and mock the package_data function to return either an empty dictionary or a custom dictionary as needed. 
- updateDatabase_unittest.py: This unit test checks if the updateDatabase function properly updates the database by serializing data and writing it to a temporary file, followed by replacing the original file. The test case uses MagicMock instances for NamedTemporaryFile, the os.replace function, and the package_data function. It also uses mock_open to mock the file writing process.
- After finishing the unit tests, we ran the unit tests to make sure that they all passed. We also did a practice run of the demo so that we are prepared for the demo day in class. So, we've successfully completed the project!