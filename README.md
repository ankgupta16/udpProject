**udpProject**  
This project is a simple UDP client-server application that sends and receives messages between the client and the server. The client sends a message to the server, and the server responds with an acknowledgment message. The client and server are implemented using Python's socket programming library. By using the UDP protocol, the client and server can communicate over a network without establishing a connection. The project demonstrates how to create a UDP client and server, send and receive messages, and handle errors and exceptions in the communication process. 
By using this project a new user can be registered to the server with Name, Surname, email, Phone Number. Email is mandatory for Register a new user and other fields are optional. The server will store the user information in a dictionary and send the acknowledgment message to the client. The client can also request to get the registered users & server will send the information, This information will be printed in json format on console. For a registered user can be deleted by passing the Email id.

To run the provided code, follow these steps:
1. Clone the repository to your local machine.  
https://github.com/ankgupta16/udpProject.git
2. Navigate to the directory containing the Python script and input files.
3. go to the project directory  
   cd udpProject
4. install the required packages  
   pip install -r requirements.txt
5. Open the terminal or command prompt and navigate to the directory containing the Python script and input files.
6. Execute the Script: Run the server script by executing the command:  
      **python server.py**
7. Execute the Script: Run the client script by executing the command on another terminal or command prompt:  
      **python client.py**
8. Choose the Choice of operation: 
9. For New User registration : Insert 1 & Enter the user details in the client console. Email is mandatory for registering a new user.
9. To get Registered Users: Insert 2 in the client console & registered users' information will be printed on console in json format.
10. TO Delete a User: Insert 3 in the client console & Enter the email id of the user to be deleted in the client console.
11. To Exit insert 4.
11. Review the Output: Check the console output for the acknowledgment messages and the registered users' information.  
**Development Environment**  
Python 3.9.7  