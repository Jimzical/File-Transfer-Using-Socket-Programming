import os
import socket
import re
import json

def InitializeClient(ip,port = 4455,filename = "file.txt",size = 1024,format = "utf-8"):
    '''
    This function is used to create a client socket and connect to the server
    '''
    addr = (ip,port)
    filesize = os.path.getsize(filename)
    client_data = {"ip":ip,"port":port,"filename":filename,"filesize":filesize,"size":size,"format":format,"addr":addr}
    return client_data


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
        nickname = input("Enter your nickname: ")
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


def main():
    # ip = "192.168.235.1"
    ip = input("Enter Server Ip Address or Nickname:")
    ip = ip_verify(ip)

    if ip:        
        client_data = InitializeClient(ip)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print(client_data["addr"])
        client.connect(client_data["addr"]) 

        data = "{}_{}".format(client_data["filename"],client_data["filesize"])
        client.send(data.encode(client_data["format"])) #encodes the data in utf-8 and sends it to the server

        msg = client.recv(client_data["size"]).decode(client_data["format"]) #To receive acknowledgement msg from server
        print(f"SERVER: {msg}") #Decodes and prints the message


    f = open(client_data["filename"], "r") 

    while True:
        data = f.read(client_data["size"])
        if not data:
            break
        client.send(data.encode(client_data["format"]))
        msg = client.recv(client_data["size"]).decode(client_data["format"])
    
    client.close()
    f.close()

if __name__ == "__main__":
    main()






    

    
