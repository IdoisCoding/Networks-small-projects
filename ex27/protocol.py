from pathlib import Path

LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    commands = ["DIR", "DELETE", "COPY", "EXECUTE"]

    if data == "TAKE_SCREENSHOT" or data == "EXIT":
        return True

    if data.startswith("COPY C:\\"):
        try:
            first_path_start = data.index('C:\\')
            second_path_start = data.index('C:\\', first_path_start + 1)
            if first_path_start != -1 and second_path_start != -1:
                return True
        except ValueError:
            return False

    for cmd in commands:
        if data.startswith(f"{cmd} C:\\"):
            return True

    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    # (4)

    length = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    return (length + data).encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """

    # (5)

    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if not length.isnumeric():
        return False, "Error"  # Handle client disconnection

    # Read actual message
    data = my_socket.recv(int(length)).decode()

    return True, data