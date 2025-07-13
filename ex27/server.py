import pyautogui
import glob
import os
import socket
import protocol
import shutil
import subprocess

IP = "127.0.0.1"
PHOTO_PATH = "C:\\networks\\network_work\\server_space\\testEx27.png" # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    if not protocol.check_cmd(cmd):
        return False, "", []

    if cmd == "TAKE_SCREENSHOT" or cmd == "EXIT":
        return True, cmd, []

    # Handle commands with parameters
    commands = ["DIR", "DELETE", "EXECUTE"]
    for command in commands:
        if cmd.startswith(f"{command} "):
            param = cmd[len(command) + 1:]  # Get everything after "COMMAND "
            if param.startswith("C:\\"):
                return True, command, [param]

    # Special handling for COPY which has two parameters
    if cmd.startswith("COPY "):
        try:
            # Find the two paths in the command
            first_path_start = cmd.index('C:\\')
            second_path_start = cmd.index('C:\\', first_path_start + 2)

            # Extract the two paths
            first_path = cmd[first_path_start:second_path_start].strip()
            second_path = cmd[second_path_start:].strip()

            return True, "COPY", [first_path, second_path]
        except ValueError:
            return False, "", []

    return False, "", []


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data as a string

    """
    response = ""

    if command == "DIR":
        files = glob.glob(params[0] + r"\*.*")
        # Convert list of files to a string with one file per line
        response = '\n'.join(files) if files else "No files found"

    elif command == "DELETE":
        try:
            os.remove(params[0])
            response = 'Deleted ' + params[0]
        except Exception as e:
            response = f'Error deleting file: {str(e)}'

    elif command == 'COPY':
        try:
            shutil.copy(params[0], params[1])
            response = 'Copied: ' + params[0] + " to " + params[1]
        except Exception as e:
            response = f'Error copying file: {str(e)}'

    elif command == "EXECUTE":
        try:
            subprocess.call((params[0]))
            response = 'Executed ' + params[0]
        except Exception as e:
            response = f'Error executing file: {str(e)}'

    elif command == 'TAKE_SCREENSHOT':
        try:
            image = pyautogui.screenshot()
            image.save(PHOTO_PATH)
            response = str(os.path.getsize(PHOTO_PATH))
        except Exception as e:
            response = f'Error taking screenshot: {str(e)}'

    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Use TCP (SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))  # Bind to IP and port

    # Start listening for incoming connections
    server_socket.listen(1)  # 1 connection at a time (adjust if needed)
    print("Server is waiting for a connection...")

    # Accept client connection
    client_socket, addr = server_socket.accept()  # Wait for client to connect
    print(f"Connection established with {addr}")

    # Handle requests until user asks to exit
    while True:
        try:
            # Check if protocol is OK, e.g. length field OK
            valid_protocol, cmd = protocol.get_msg(client_socket)
            if valid_protocol:
                # Check if params are good, e.g. correct number of params, file name exists
                valid_cmd, command, params = check_client_request(cmd)
                if valid_cmd:
                    if command == 'EXIT':
                        # Send confirmation before breaking
                        response = "Goodbye!"
                        client_socket.send(protocol.create_msg(response))
                        break

                    if command == 'TAKE_SCREENSHOT':
                        response = handle_client_request(command, params)
                        # First send the length as a protocol message
                        client_socket.send(protocol.create_msg(response))
                        # Then send the actual file
                        with open(PHOTO_PATH, 'rb') as f:
                            client_socket.sendall(f.read())
                    else:
                        response = handle_client_request(command, params)
                        client_socket.send(protocol.create_msg(response))
                else:
                    # Prepare proper error to client
                    response = 'Bad command or parameters'
                    client_socket.send(protocol.create_msg(response))
            else:
                # Prepare proper error to client
                response = 'Packet not according to protocol'
                client_socket.send(protocol.create_msg(response))
        except Exception as e:
            print(f"Error in server loop: {str(e)}")
            response = f"Server error: {str(e)}"
            try:
                client_socket.send(protocol.create_msg(response))
            except:
                print("Could not send error message to client")
            break

    # Close the client socket after finishing the communication
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()