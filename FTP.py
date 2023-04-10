import os
import socket
import re
import json
def InitializeClient(ip,filename = "file.txt",port = 4455,size = 1024,format = "utf-8"):
    '''
    This function is used to create a client socket and connect to the server
    '''
    addr = (ip,port)
    filesize = os.path.getsize(filename)
    client_data = {"ip":ip,"port":port,"filename":filename,"filesize":filesize,"size":size,"format":format,"addr":addr}
    return client_data

def InitializeServer():
    ip = socket.gethostbyname(socket.gethostname()) #To get IP address of the local host
    port = 4455
    addr = (ip, port)
    size = 1024
    format = "utf-8"

    server_data = {"ip":ip,"port":port,"addr":addr,"size":size,"format":format}
    return server_data



def ip_verify(ip):
    '''
    Using Regular Expression to verify the IP Address
    '''
    # if nicknames.json doesnt exist make one
    if not os.path.exists("nicknames.json"):
        with open("nicknames.json","w") as f:
            json.dump({},f)

    # read nicknames.json
    with open("nicknames.json","r") as f:
        nicknames = json.load(f)
    # check if ip is in nicknames.json
    if ip in nicknames:
        print("Welcome Back {} ({})".format(ip,nicknames[ip]))
        ip = nicknames[ip]
        return ip
    else:
        nickname = input("Create a  handle: ")
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if pattern.match(ip):
            print("IP Address Verified")
            nicknames[nickname] = ip
            with open("nicknames.json","w") as f:
                json.dump(nicknames,f)
                print("Welcome {}".format(nickname))
            return ip
        else:
            print("Invalid IP Address")
            print("Transfer Failed")
            return False

def Client():
    ip = input("Enter Server Ip Address or Handle:")
    ip = ip_verify(ip)
    filename = input("Enter Filename: ")

    # if file name does not end in .txt or .py or .c add .txt
    if not filename.endswith(".txt") and not filename.endswith(".py") and not filename.endswith(".c"):
        filename += ".txt"

    if ip:        
        client_data = InitializeClient(ip,filename=filename)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect(client_data["addr"]) 
        data = "{}_{}".format(client_data["filename"],client_data["filesize"])
        
        client.send(data.encode(client_data["format"])) #encodes the data in utf-8 and sends it to the server

        msg = client.recv(client_data["size"]).decode(client_data["format"]) #To receive acknowledgement msg from server
        print(f"SERVER:\nFile Content\n----------------\n{msg}\n----------------") #Decodes and prints the message

        # f = open(client_data["filename"], "r") 

        # while True:
        #     data = f.read(client_data["size"])
        #     if not data:
        #         break
        #     client.send(data.encode(client_data["format"]))
        #     msg = client.recv(client_data["size"]).decode(client_data["format"])
        # f.close()
        client.close()
    else:
        print("Transfer Failed")

def Server():
    server_data = InitializeServer()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #AF_INET is used to designate the type of IP address the socket communicates in (Here it's IPv4)
    #SOCK_STREAM specifies that is a TCP socket. 

    server.bind(server_data["addr"]) #Assign the IP address and port number to the socket instance we created
    server.listen()

    print("Server is listening...")

    conn, address = server.accept()
    print(f"Client connected from {address[0]}:{address[1]} ")

    data  = conn.recv(server_data["size"]).decode(server_data["format"])

    data = data.split("_")[0]       # To retrieve the filename from the data received rather than the filename_filesize

    # check if data in format filename_filesize
    pattern = re.compile(r"^(?:[a-zA-Z0-9]+_){1}[0-9]+$")
    if not pattern.match(data):
        # send the file back to the client
        print("Sending file to client")
        with open("recived_files/recv_{}".format(data),"r") as f:
            data = f.read()
        conn.send(data.encode(server_data["format"]))


    else:

        item = data.split("_") #To retrieve file name and file size from the data received
        filename = item[0]

        conn.send("Filename and file size received".encode(server_data["format"]))

        #progress = tqdm(range(filesize), f"Receiving {filename}", unit = "B", unit_scale = True, unit_divisor = filesize )
        # if folader called recived_files does not exist, make it
        if not os.path.exists("recived_files"):
            os.mkdir("recived_files")

        f = open("recived_files/recv_{}".format(filename),"w")

        while True:
            data = conn.recv(server_data["size"]).decode(server_data["format"])

            if not data:
                break

            f.write(data)
            conn.send("data received".encode(server_data["format"]))

        f.close()
        # print file contents
        with open("recived_files/recv_{}".format(filename),"r") as f:
            print("File Contents:")
            print("--------------")
            print(f.read())
            print("--------------")

        print("File sent successfully")  

    conn.close()
    server.close()
    f.close()


def main():
    # ip = "192.168.235.1"

    choice = input('''
    Choose an option:
    1. Client
    2. Server
    ''')

    # switch case
    if choice == "1":
        Client()
    elif choice == "2":
        Server()
    



if __name__ == "__main__":
    main()






    

    

    # q:what does push do in git
    # a:   
