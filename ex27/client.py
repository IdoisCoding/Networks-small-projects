import os
import socket
import protocol


IP = "127.0.0.1"
SAVED_PHOTO_LOCATION = "C:\\networks\\network_work\\testEx27\\testEx27.png" # The path + filename where the copy of the screenshot at the client should be saved

def handle_server_response(my_socket, cmd):
    success, response = protocol.get_msg(my_socket)

    if not success:
        print("Error receiving data.")
        return

    if cmd == 'TAKE_SCREENSHOT':
        # Response is the length of the photo
        try:
            photo_len = int(response)
            with open(SAVED_PHOTO_LOCATION, 'wb') as f:
                remaining = photo_len
                while remaining > 0:
                    data = my_socket.recv(min(4096, remaining))
                    if not data:
                        break
                    f.write(data)
                    remaining -= len(data)
            print(f"Screenshot saved to: {SAVED_PHOTO_LOCATION}")
            os.startfile(SAVED_PHOTO_LOCATION)
        except ValueError as e:
            print(f"Error processing screenshot: {str(e)}")
    else:
        print(response)

def main():
    # open socket with the server
    my_socket = socket.socket()
    my_socket.connect((IP, 8820))

    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()

if __name__ == '__main__':
    main()
