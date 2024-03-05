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
    data_sock.connect("raspberrypi.local",37444)
    data_sock.settimeout(-1)
    flag_sock.settimeout(30)
    flag_sock.connect("raspberrypi.local",37444)
    flag_sock.settimeout(-1)
    
def end_wireless():
    global data_sock,flag_sock
    
    