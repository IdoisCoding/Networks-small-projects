import socket
import protocol

IP = "127.0.0.1"
def main():
    port = protocol.STARTING_PORT
    while(True):
        socketA1 = socket.socket() # create socket
        socketA1.bind((IP, int(port))) # bind the server to the ip and port
        socketA1.listen()
        print("Side A listening to port ", port)
        socketB, addr = socketA1.accept()
        print("Side B connecting to port ", port)
        valid_protocol, cmd = protocol.get_msg(socketB)
        valid_port, port = protocol.get_port(cmd)
        if valid_protocol == False or cmd == "exit" or valid_port == False :
            break
        else:
            print("Side B: ", cmd)
        print("Side B disconnected")
        socketA1.close()
        socketB.close()
        print("Side B listening to port ", port)
        socketA2 = socket.socket()
        socketA2.connect((IP, int(port)))
        print("Side A connecting to port ", port)
        #cmd = input("write a message (include a valid port)")
        cmd = "Hello World"
        print("Side A: ", cmd)
        mesg, port = protocol.create_msg(cmd)
        socketA2.send(mesg)
        print("Side A disconnected")
        if (cmd == 'exit'):
            break

if __name__ == "__main__":
    main()



