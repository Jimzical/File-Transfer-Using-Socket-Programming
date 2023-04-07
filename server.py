import os
import socket
from tqdm import tqdm

ip = socket.gethostbyname(socket.gethostname()) #To get IP address of the local host
port = 4455
addr = (ip, port)
size = 1024
format = "utf-8"


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #AF_INET is used to designate the type of IP address the socket communicates in (Here it's IPv4)
    #SOCK_STREAM specifies that is a TCP socket. 

    server.bind(addr) #Assign the IP address and port number to the socket instance we created
    server.listen()

    print("Sever is listening...")

    conn, address = server.accept()
    print(f"Client connected from {address[0]}:{address[1]} ")

    data  = conn.recv(size).decode(format)
    print(data)

    item = data.split("_") #To retrieve file name and file size from the data received
    filename = item[0]
    filesize = item[1]

    conn.send("Filename and file size received".encode(format))

    #progress = tqdm(range(filesize), f"Receiving {filename}", unit = "B", unit_scale = True, unit_divisor = filesize )


    f = open(f"recv_{filename}","w")

    while True:
        data = conn.recv(size).decode(format)

        if not data:
            break

        f.write(data)
        conn.send("data received".encode(format))

        #progress.update(len(data))
    
    
    conn.close()
    server.close()
    f.close()

if __name__ == "__main__":
    main()



