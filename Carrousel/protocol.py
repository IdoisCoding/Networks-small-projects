import socket
import random

LENGTH_FIELD_SIZE = 4
STARTING_PORT = 8820
def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    port = ""
    if(data != "exit"):
        hasPort, port = get_port(data)
        if(hasPort == False):
            port = random.randint(1025,49150) #add random port
            data = data + str(port)
    length = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    return (length + data).encode(), port

def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """

    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if not length.isnumeric():
        return False, "Error"  # Handle client disconnection

    # Read actual message
    data = my_socket.recv(int(length)).decode()

    return True, data

def get_port(mesg):
    if(len(mesg) < 4):
        return False, "Error"  # Handle client disconnection
    port = mesg[len(mesg) - 4:]
    if(port.isnumeric() == False):
        return False, "Error" # Handle client disconnection
    if(len(mesg) >= 5 and mesg[len(mesg) - 5].isnumeric()):
        port = mesg[len(mesg) - 5] + port # Port has 5 digits
    if (int(port) <= 1024 or int(port) >= 49151 or int(port) == 10000):
        return False, "Illegal range"  # Handle client disconnection
    return True, port
