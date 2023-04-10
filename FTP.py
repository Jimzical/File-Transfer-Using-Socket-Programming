import os
import socket
import re
import json
import streamlit as st
def InitializeClient(ip,filename = "file.txt",port = 4455,size = 1024,format = "utf-8"):
    '''
    This function is used to create a client socket and connect to the server
    '''
    addr = (ip,port)
    filesize = os.path.getsize(filename)
    client_data = {"ip":ip,"port":port,"filename":filename,"filesize":filesize,"size":size,"format":format,"addr":addr}
    return client_data

def InitializeServer(port = 4455,size = 1024,format = "utf-8"):
    ip = socket.gethostbyname(socket.gethostname()) #To get IP address of the local host
    addr = (ip, port)
    server_data = {"ip":ip,"port":port,"addr":addr,"size":size,"format":format}
    return server_data


def CheckNicknames():
    '''
    Check if nicknames.json exists and if not create it and return the nicknames
    '''
    if not os.path.exists("nicknames.json"):
        with open("nicknames.json","w") as f:
            json.dump({},f)

    with open("nicknames.json","r") as f:
        nicknames = json.load(f)
    return nicknames

def ip_verify(ip):
    '''
    Using Regular Expression to verify the IP Address
    '''

    nicknames = CheckNicknames()
    
    # check if ip is in nicknames.json
    if ip in nicknames:
        print("Welcome Back {} ({})".format(ip,nicknames[ip]))
        st.markdown("## Welcome Back {} ({})".format(ip,nicknames[ip]))
        ip = nicknames[ip]
        return ip

    else:
        print("Invalid IP Address")
        print("Transfer Failed")
        st.markdown("## Invalid IP Address")
        st.markdown("## Transfer Failed")
        return False

def Client(ip,filename):
    ip = ip_verify(ip)

    # if file name does not end in .txt or .py or .c add .txt
    if not filename.endswith(".txt") and not filename.endswith(".py") and not filename.endswith(".c"):
        filename += ".txt"

    if ip:        
        client_data = InitializeClient(ip,filename=filename,port=4456)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        client.connect(client_data["addr"]) 
        data = "{}_{}".format(client_data["filename"],client_data["filesize"])
        
        client.send(data.encode(client_data["format"])) #encodes the data in utf-8 and sends it to the server

        msg = client.recv(client_data["size"]).decode(client_data["format"]) #To receive acknowledgement msg from server
        print(f"SERVER:\nFile Content\n----------------\n{msg}\n----------------") #Decodes and prints the message
        st.markdown(f"## SERVER:\nFile Content\n----------------\n{msg}\n----------------")

        client.close()
    else:
        print("Transfer Failed")

def Server():
    server_data = InitializeServer(port=4456)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    server.bind(server_data["addr"]) #Assign the IP address and port number to the socket instance we created
    server.listen()

    print("Server is listening...")
    st.caption("## Server is listening...")

    conn, address = server.accept()
    
    print(f"Client connected from {address[0]}:{address[1]} ")
    st.markdown(f"## Client connected from {address[0]}:{address[1]} ")

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

def MakeNicknames(ip,nickname):
    nicknames = CheckNicknames()
    sub = st.button("Submit",key="submit")
    if sub:
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if pattern.match(ip):
            print("IP Address Verified")
            st.caption("IP Address Verified")

            nicknames[nickname] = ip
            with open("nicknames.json","w") as f:
                json.dump(nicknames,f)

                print("Welcome {}".format(nickname))
                st.markdown("## Welcome {}".format(nickname))
            return ip
        else:
            print("Invalid IP Address")
            st.caption("Invalid IP Address")
            return False

def BuildGUI():
    nick = CheckNicknames()
    nickname_list = list(nick.keys())

    # Add custom CSS to app
    button_style = """
        <style>
            div.stButton > button:first-child {
                padding: 0.75rem 3rem;
                font-size: 50 em;
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    st.title("FTP")
    st.subheader("File Transfer Protocol")
    st.markdown("This is a simple FTP program that allows you to send files from one computer to another over a network.")
    st.markdown("This program uses TCP sockets to send files.")

    # make a sidebar
    st.sidebar.title("MODE")

    mode = st.sidebar.radio("Choose Mode",("Client","Server","Create Alias"))
    if mode == "Client":
        st.subheader("Client")
        ip = st.selectbox("Enter Server IP Address or Handle: ",nickname_list)
        # ip = st.text_input("Enter Server IP Address or Handle: ")
        # st.progress(0)  
        filename = st.text_input("Enter Filename: ")

        if st.button("Send File"):
            Client(ip,filename)

    elif mode == "Server":
        st.subheader("Server")
        if st.button("Start Server"):
            Server()
    elif mode == "Create Alias":
        st.subheader("Nickname")
        ip = st.text_input("Enter IP Address: ")
        nickname = st.text_input("Create a  handle: ")

        MakeNicknames(ip,nickname)

    # if st.sidebar.button("Client"):
    #     st.subheader("Client")
    #     ip = st.text_input("Enter Server IP Address or Handle: ")

    #     # ip = st.text_input("Enter Server IP Address or Handle: ")
    #     filename = st.text_input("Enter Filename: ")

    #     if st.button("Send File"):
    #         Client(ip,filename)

    # if st.sidebar.button("Server"):
    #     st.subheader("Server")
    #     if st.button("Start Server"):
    #         Server()



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
    # main()
    BuildGUI()




