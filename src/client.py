import socket
import json
from src.utils.config_parser import ConfigParser

config = ConfigParser()
host = config.get_prop_value('SERVER_INFORMATION', 'host')
port = int(config.get_prop_value('SERVER_INFORMATION', 'port'))
data_payload = int(config.get_prop_value('SERVER_INFORMATION', 'data_payload_size'))


def send_message(message_type, data):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    try:
        # Send data
        message = json.dumps({'type': message_type, 'data': data})
        print("Sending %s" % message)
        is_sent = False
        try:
            sock.settimeout(2)
            sock.sendto(message.encode('utf-8'), server_address)
            is_sent = True
            print("Message sent successfully")
        except socket.timeout:
            # Handle timeout error
            print("Timeout occurred while sending message")
        except OSError as e:
            # Handle the error if sending fails
            print(f"Error occurred while sending message: {e}")
        except Exception as e:
            # Handle other errors
            print(f"An error occurred: {e}")
        finally:
            sock.settimeout(None)

        if is_sent:
            try:
                sock.settimeout(5)
                # Receive response
                data, server = sock.recvfrom(data_payload)
                if message_type == 'GET_USERS':
                    print(json.dumps(json.loads(data)))
                else:
                    print("received %s" % json.loads(data))
            except socket.timeout:
                # Handle timeout error
                print("Timeout occurred while receiving message from the server..")
            except OSError as e:
                # Handle other socket-related errors
                print(f"Error : Socket error occurred while receiving message - {e.strerror}")
            finally:
                sock.settimeout(None)

    finally:
        print("Closing connection to the server")
        sock.close()


if __name__ == '__main__':

    while True:
        operation_choice = input("enter the choice of operation: 1. Register User 2. Get Users 3. Delete User 4. Exit \n")
        if operation_choice == '4':
            exit(0)
        elif operation_choice == '1':
            message_type = 'REGISTER_USER'
            user_name = input("Enter the user name: ")
            user_surname = input("Enter the user surname: ")
            user_email = input("Enter the user email: ")
            user_phone = input("Enter the user phone: ")
            user_data = {'Email': user_email, 'Name': user_name, 'Surname': user_surname, 'PhoneNumber': user_phone}
            if user_email is None or user_email.strip() == "":
                print("Email is required to register user. Please try again.")
                continue
            send_message(message_type, user_data)
        elif operation_choice == '2':
            send_message('GET_USERS', None)
        elif operation_choice == '3':
            email = input("Enter the email of the user to delete: ")
            send_message('DELETE_USER', {'Email': email})
        else:
            print("Invalid choice of operation. Please try again.")
            exit(0)
