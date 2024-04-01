import socket
import json
from src.utils.config_parser import ConfigParser

# Initialize configuration
config = ConfigParser()
host = config.get_prop_value('SERVER_INFORMATION', 'host')
port = int(config.get_prop_value('SERVER_INFORMATION', 'port'))
data_payload = int(config.get_prop_value('SERVER_INFORMATION', 'data_payload_size'))

# Dictionary to store registered users
registered_users = {}


def send_response(sock, address, data):
    """Send a response to the client."""
    try:
        sent = sock.sendto(json.dumps(data).encode('utf-8'), address)
        print(f"Sent {sent} bytes back to {address}")
    except OSError as e:
        print(f"Error occurred while sending response: {e}")


def send_error_response(sock, address, error_message):
    """Send an error response to the client."""
    error_data = {'ERROR': error_message}
    send_response(sock, address, error_data)


def register_user(sock, address, message_data):
    """Register a new user or update existing user information."""
    if 'Email' not in message_data:
        error_message = "Error: Email is required to register user."
        send_error_response(sock, address, error_message)
        return

    email = message_data['Email'].strip()
    if email in registered_users:
        update_user_info(sock, address, email, message_data)
    else:
        add_new_user(sock, address, email, message_data)


def update_user_info(sock, address, email, message_data):
    """Update existing user information."""
    info_updated = 0
    for key in ['Name', 'Surname', 'PhoneNumber']:
        if key in message_data:
            new_value = message_data[key]
            if new_value != registered_users[email].get(key, ''):
                registered_users[email][key] = new_value
                info_updated += 1

    if info_updated > 0:
        response_data = {
            "REGISTRATION_DONE": f"User {email} updated successfully with data {registered_users[email]}"
        }
    else:
        response_data = {
            "REGISTRATION_DONE": f"User {email} already exists with data {registered_users[email]}"
        }
    send_response(sock, address, response_data)


def add_new_user(sock, address, email, message_data):
    """Add a new user."""
    user_data = {'Name': '', 'Surname': '', 'Email': email, 'PhoneNumber': ''}
    for key in ['Name', 'Surname', 'PhoneNumber']:
        if key in message_data:
            user_data[key] = message_data[key]
    registered_users[email] = user_data
    response_data = {
        "REGISTRATION_DONE": f"User {email} registered successfully with data {user_data}"
    }
    send_response(sock, address, response_data)


def delete_user(sock, address, message_data):
    """Delete a user."""
    if 'Email' not in message_data:
        error_message = "Error: Email is required to delete user."
        send_error_response(sock, address, error_message)
        return

    email = message_data['Email'].strip()
    if email not in registered_users:
        error_message = "Error: User not found with this email."
        send_error_response(sock, address, error_message)
        return

    del registered_users[email]
    response_data = {
        "DELETION_DONE": f"User {email} deleted successfully."
    }
    send_response(sock, address, response_data)


def get_users(sock, address):
    """Send list of registered users."""
    response_data = {
        "USERS": registered_users
    }
    send_response(sock, address, response_data)


def process_message(sock, address, received_message):
    """Process the received message."""
    try:
        message = json.loads(received_message)
        if 'type' in message and 'data' in message:
            message_type = message['type']
            message_data = message['data']
            if message_type == 'REGISTER_USER':
                register_user(sock, address, message_data)
            elif message_type == 'DELETE_USER':
                delete_user(sock, address, message_data)
            elif message_type == 'GET_USERS':
                get_users(sock, address)
            else:
                error_message = "Error: Please send correct message type, only 'REGISTER_USER', 'DELETE_USER', and 'GET_USERS' operations are accepted."
                send_error_response(sock, address, error_message)
        else:
            error_message = "Error: Please send correct format, only JSON format message is accepted which should contain 'type' and 'data' keys."
            send_error_response(sock, address, error_message)
    except json.JSONDecodeError:
        error_message = "Error: Please send correct format, only JSON format is accepted."
        send_error_response(sock, address, error_message)


def server_processing():
    """Start the server and process incoming messages."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    print("Starting up echo server on %s port %s" % server_address)

    try:
        sock.bind(server_address)
        while True:
            print("Waiting to receive message from client")
            message, address = sock.recvfrom(data_payload)
            print("Received %s bytes from %s" % (len(message), address))
            if message:
                received_message = message.decode('utf-8')
                print(received_message)
                process_message(sock, address, received_message)
    except OSError as e:
        print(f"Socket operation failed: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    server_processing()
