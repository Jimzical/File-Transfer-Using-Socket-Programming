import os
import socket
from tqdm import tqdm

ip = socket.gethostbyname(socket.gethostname()) #To get IP address of the local host
port = 4455
addr = (ip, port)
size = 1024
format = "utf-8"

filename = "file.txt"
filesize = os.path.getsize(filename)



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #AF_INET is used to designate the type of IP address the socket communicates in (Here it's IPv4)
    #SOCK_STREAM specifies that is a TCP socket.

    client.connect(addr) #To connect to the server 

    data = f"{filename}_{filesize}"
    client.send(data.encode(format)) #encodes the data in utf-8 and sends it to the server

    msg = client.recv(size).decode(format) #To receive acknowledgement msg from server
    print(f"SERVER: {msg}") #Decodes and prints the message

   # progress = tqdm(range(filesize), f"Sending {filename}", unit = "B", unit_scale = True, unit_divisor = filesize )

    f = open(filename, "r") 

    while True:
        data = f.read(filesize)

        if not data:
            break

        client.send(data.encode(format))
        msg = client.recv(filesize).decode(format)

        #progress.update(len(data))
    
    client.close()
    f.close()

if __name__ == "__main__":
    main()






    

    