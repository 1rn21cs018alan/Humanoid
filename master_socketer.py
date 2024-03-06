import socket,struct

#constants
_SLOW=1
_SLOW_ACTION=2
_INTERRUPT=3
_LOAD=4
_PLAY=5
_TERMINATE=2003
_End_Mark=struct.pack("!i",203144)
data_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
flag_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def connect():
    global data_sock,flag_sock
    data_sock.settimeout(30)
    flag_sock.settimeout(30)
    server_port=("127.0.0.1",37444) # use this to run on local machine
    #server_port=("192.168.1.1",37444) # use this if running on rasp
    
    data_sock.connect(server_port)
    flag_sock.connect(server_port)
    
def end_wireless():
    global data_sock,flag_sock
    data_sock.send(struct.pack("!i",_TERMINATE))
    data_sock.close()
    flag_sock.close()
    
# connect()
# input("enter")
# end_wireless()
def slow(initialpos,delay=100,steps=6):
    global data_sock
    if type(initialpos)!=list and type(initialpos)!=tuple:
        raise TypeError("Not a list/tuple") 
    elif len(initialpos)!=16:
        raise ValueError("Not 16 angles")
    send_data=struct.pack("!3i16f",_SLOW,steps,delay,*initialpos)
    data_sock.send(send_data)
    
def slow_action(initialpos,finalpos,delay=100,steps=6):
    global data_sock
    if type(initialpos)!=list and type(initialpos)!=tuple:
        raise TypeError("Not a list/tuple") 
    elif len(initialpos)!=16:
        raise ValueError("Not 16 angles")
    if type(finalpos)!=list and type(finalpos)!=tuple:
        raise TypeError("Not a list/tuple") 
    elif len(finalpos)!=16:
        raise ValueError("Not 16 angles")
    send_data=struct.pack("!2i32f",_SLOW_ACTION,steps,delay,*initialpos,*finalpos)
    data_sock.send(send_data)
    
def load(steps):
    global data_sock
    if type(steps)!=list and type(steps)!=tuple:
        raise TypeError("Not a list/tuple") 
    n=len(steps)
    if n==0:
        return
    send_data=[n]
    for each in steps:
        if type(each)!=list and type(each)!=tuple:
            raise TypeError("Not a list/tuple") 
        elif len(each)!=16:
            raise ValueError("Not 16 angles")
        send_data.extend(each)
    send_data=struct.pack(f"!3i{n*16}f",_LOAD,n,*send_data)
    data_sock.send(send_data)
    
def play(intermediate_steps=6,delay=100):
    global data_sock
    send_data=struct.pack("!3i",_PLAY,intermediate_steps,delay)
    data_sock.send(send_data)
    
def interrupt():
    global flag_sock
    flag_sock.send(struct.pack("!i",2003))
    