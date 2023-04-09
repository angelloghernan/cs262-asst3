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


`python logical_clocks.py` or `python3 logical_clocks.py`

You don't need to use pip to install any packages. This was originally wrote for and run on Python 3.9.13. 

After two minutes have elapsed, the simulation will stop running automatically (no more output will be printed to the terminal or logged). Press Ctrl+C to shut it down.


# About 
We fully implemented the specification on Canvas. We created a simulation of a small distributed system containing three machines with varying clock speeds, which can be set by a random seed. Each machine connects to each other in a pre-specified order and begins sending out messages randomly to both of its neighboring machines in the network randomly. 

Each clock cycle, a machine reads its pending messages from its queue (if any) and updates its logical clock based on the logical clock number it has received from  neighboring machines. If there are none pending, it randomly may either send a message to one of the machines or both or update its own logical clock internally.

See `engineering_notebook.md` for more details on the decision-making process simulation design and its results.


# Testing
To run the unit test, simply run the command

python3 -m unittest unittest_FUNCTION_TO_BE_TESTED.py
    
There are four files to run the unit test. The test is conducted on presumed input spaces without much testing on non-benign/malicious inputs since our functions are embedded for use in parent functions and the values, such as id, is typically fixed, and there is of limited significance to test most of these inputs. More test cases can be added simply by adding more test functions under the test class.


python GUI_chat_client.py
python GUI_chat_server_test_ver2.py 

test_load_database unittest: This test case checks whether the loadDatabase function correctly reads a pickled file and calls the unpackage_data function with the correct arguments.

The unittest alsot checks if the loadDatabase function raises an exception when the pickled data is invalid (e.g., corrupted or not a pickled file), and checks if the loadDatabase function correctly reads a pickled file with a custom server name, and whether the pickle.load function is called.

We also have test case to check if the get_timestamp function returns the correct Unix timestamp (seconds since the epoch) value based on the current time in the UTC timezone. Moreover, we check if the send_pickled_data function sends the serialized data correctly over a socket connection. They use MagicMock instances for sockets and mock the package_data function to return either an empty dictionary or a custom dictionary as needed. Finally, we check if the updateDatabase function properly updates the database by serializing data and writing it to a temporary file, followed by replacing the original file. The test case uses MagicMock instances for NamedTemporaryFile, the os.replace function, and the package_data function. It also uses mock_open to mock the file writing process.

let A B C be servers, if client X wants to message Y, then X sends message to A B AND C, A B C all log same stuff, then only A sends message to Y 

# Engineering Notebook
# Day 1: 2-27
- Preface: We wrote our last project in C++, which was good for writing our own code but wasn't good for linking gRPC and running it, since we had to deal with cmake and incomplete/non-existent documentation.
- Although we aren't using any libraries this time, we decided to write the project in Python since Albert and Dean aren't as familiar with C++ and this is a shorter term project (much smaller code size as well). We also wanted to see how using Python compared to using C++, and overall we liked how Python's strengths as a language in general (concise, readable, fast to write, etc.) were reflected in the project.
- This day, we just got familiar with sockets in Python and sketched out exactly what it was we needed to do for the project (since some of the details weren't so clear).
- We decided to have three peers connect to each other using sockets (using a pre-defined ordering and ports), with threads designated to reading from the sockets on each VM (virtual machine), otherwise nothing too special. All the other details were essentially decided by the project spec, so there's not much to note there.

# Day 2: 3-1
- We reviewed the content from class about logical clocks. 
- We basically finished the server code this day. There were some issues getting the ordering to work correctly, involving a while True loop that would repeatedly attempt to connect the servers to each other if a connection failed (if, for example, one of the forked processes ran in the wrong order, this would lead to a failed connection).
- We added color-coding to the terminal output to make it easier to read and understand which VM is sending/receiving messages. This was helpful for checking our code and debugging, especially for network related code.
- Otherwise, everything went smoothly. Compared to the first project, the details here are more well-defined, so there's less need for any rewrites. It's also all of our own code, so no need to dive into documentation beyond the pages on Python sockets and threads.

# Day 3: 3-2
- Project is officially finished, besides unit testing. For unit testing, we are mostly concerned with making sure the logical clocks work correctly and sync up.
- We also added a random seed to the program, so that we can run the program multiple times and get the same results. This is useful for testing and debugging. 
- We used this random seed to test our program with different clock rates for each VM. We found that the logical clocks were able to sync up correctly, even with different clock rates, as desired.
- We then studied and analyzed our program and its logs to do the analysis outlined in the specification, and put it in the below Observations section.

# Day 4: 3-3
- Unit test was performed on all individual functions in the program, namely, client, server, process_events, send_message, virtual_machine.
- We wrote these unit tests to make sure that the functions are working as intended. We also ran our code as a whole to make sure that the entire program is working as intended.
- Instructions for how to run the unit tests are in the `README.md` file.
- Moreover, clock value plot helper function (graph_log.py) is implemented to help visualize and support our upcoming interpretation of result. An example is shown below