import socket
import struct
import time
import os
import atexit
import threading
# print(os.getcwd())
# script_dir=os.getcwd() #path.basename(os.path.abspath(__file__))
# os.chdir(script_dir)
time.sleep(6)
import humanoid_actions
from copy import deepcopy as dcopy


_SLOW=1
_SLOW_ACTION=2
_INTERRUPT=3
_LOAD=4
_PLAY=5
_TERMINATE=2003
_End_Mark=struct.pack("!i",203144)
_Terminate_Program=False
_INTERRUPT_FLAG=False

def flag_check():
    global _INTERRUPT_FLAG
    #print("checking")
    temp=_INTERRUPT_FLAG
    _INTERRUPT_FLAG=False
    return temp

actions=humanoid_actions.Humanoid_Action_Bank()
actions.checkfunc=flag_check

#Functions Area





def Interrupt_check(inter_sock):
    global _Terminate_Program
    global _INTERRUPT_FLAG
    while not _Terminate_Program:
        Signal_type=inter_sock.recv(4)
        if not Signal_type:
            continue
        Signal_type=struct.unpack('!i',Signal_type)[0]
        if Signal_type==_INTERRUPT:
            _INTERRUPT_FLAG=True

def close_leak(): 
    client_socket.close()
    interrupt_socket.close()
    server_socket.close()
atexit.register(close_leak)


def slow(initialpos,delay,steps):
    print(initialpos,delay,steps)
    actions.slow(final_pos=initialpos,deltime=delay,steps=steps)
def slow_action(initialpos,finalpos,delay,steps):
    print(initialpos,finalpos,delay,steps)
def interrupt():
    print("interrupted")
def load(load_data):
    print(load_data)
    for i in range(len(load_data)):
        load_data[i]=list(load_data[i])
    actions.saved_states=dcopy(load_data)
def play_loaded_data(delay,steps):
    print(actions.saved_states)
    actions.checkfunc=flag_check
    print(flag_check)
    actions.Run_Preset(delay=delay,steps=steps)
    print("start playing",delay,steps)


def recieve():
    global _Terminate_Program
    Signal_type=client_socket.recv(4)
    if not Signal_type:
        _Terminate_Program=True
        return
    Signal_type=struct.unpack('!i',Signal_type)[0]
    if Signal_type==_TERMINATE:
        _Terminate_Program=True
        return True
    if Signal_type==_SLOW:
        data=struct.unpack("!2i16f",client_socket.recv(struct.calcsize("!2i16f")))
        slow(data[2:],data[1],data[0])
    elif Signal_type==_SLOW_ACTION:
        data=struct.unpack("!2i32f",client_socket.recv(struct.calcsize("!2i32f")))
        slow_action(data[2:18],data[18:],data[1],data[0])
    # elif Signal_type==_INTERRUPT:
    #     interrupt()    
    elif Signal_type==_LOAD:
        n=struct.unpack("!i",client_socket.recv(struct.calcsize("!i")))[0]
        size=n*16
        data=struct.unpack(("!"+str(size)+"f"),client_socket.recv(struct.calcsize(("!"+str(size)+"f"))))
        Steps=[]
        for i in range(n):
            Steps.append(data[i*16:(i+1)*16])
            
        load(Steps)
    elif Signal_type==_PLAY:
        data=struct.unpack("!2i",client_socket.recv(struct.calcsize("!2i")))
        play_loaded_data(data[1],data[0])
    else:
        print("none of the above",Signal_type)
    return False








#end of function Area


server_address = ("127.0.0.3", 37444) #for running locally
# server_address = ("192.168.1.1", 37444) # for running on Raspberry-Pi

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Bind the socket to the server address
server_socket.bind(server_address)

# Listen for incoming connections




try:
    server_socket.listen(2)

    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print("Connection established with", client_address)

    print("Waiting for a connection...")
    interrupt_socket, interrupt_address = server_socket.accept()
    print("Connection established with", interrupt_address)
    # server.listen(1)
    # csock,caddr=server.accept()
except socket.timeout:
    print("exiting")
    print(os.getcwd())
    with open("stuff",mode="r") as f:
        try:
            f.readline()
            a=int(f.readline())
        except:
            a=0
    with open("stuff",mode="w+") as f:
        f.write("finished running\n"+str(a+1))
    exit(0)
print(client_address)
actions.start()
interrupt_thread=threading.Thread(target=Interrupt_check,args=[interrupt_socket])
interrupt_thread.start()
time.sleep(2)
client_socket.settimeout(30)
try:
    while(not _Terminate_Program):
        if recieve():
            break
        if _INTERRUPT_FLAG:
            print("interrupted")
            # _INTERRUPT_FLAG=False
        # Print the received data
        print("Received data")
    client_socket.close()
    interrupt_socket.close()
    server_socket.close()
finally:
    client_socket.close()
    interrupt_socket.close()
    server_socket.close()
