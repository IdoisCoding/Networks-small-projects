import socket
import protocol

IP = "127.0.0.1"
def main():
    port = protocol.STARTING_PORT
    while(True):
        print("Side A listening to port ", port)
        socketB1 = socket.socket()
        socketB1.connect((IP, int(port)))
        print("Side B connecting to port ", port)
        #cmd = input("write a message (include a valid port)")
        cmd = "Hello World"
        print("Side B: ", cmd)
        mesg, port = protocol.create_msg(cmd)
        socketB1.send(mesg)
        print("Side B disconnected")
        if (cmd == 'exit'):
            break
        socketB1.close()
        socketB2 = socket.socket()  # create socket
        socketB2.bind((IP, int(port)))  # bind the server to the ip and port
        socketB2.listen()
        print("Side B listening to port ", port)
        socketA, addr = socketB2.accept()
        print("Side A connecting to port ", port)
        valid_protocol, cmd = protocol.get_msg(socketA)
        valid_port, port = protocol.get_port(cmd)
        if valid_protocol == False or cmd == "exit" or valid_port == False:
            break
        else:
            print("Side A: ", cmd)
        print("Side A disconnected")
        socketA.close()
        socketB2.close()


if __name__ == "__main__":
    main()



