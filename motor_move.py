import time
import socket
import struct
import atexit

HOST = '127.0.0.1'
PORT = 22343

def close_socket(sock):
    try:
        sock.close()
    except Exception as e:
        print("Error closing socket:", e)
# Function to convert the data to bytes
def pack_data(data):
    return struct.pack('!16f', *data)  # Using the struct module to format the data

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
Angles=[0]*16
count=0
pwm_val=[[0,0] for i in range(16)]
printerror=False
atexit.register(close_socket, client_socket)
def motor_set(motor_pin:int,pwm_min:int,pwm_max:int):
    # kit.servo[motor_pin].set_pulse_width_range(pwm_min,pwm_max)
    pwm_val[motor_pin]=[pwm_min,pwm_max]
    # with open("calib_value.txt", mode="a") as file1:
    #     file1.write(str(motor_pin)+" "+str(pwm_min)+" "+str(pwm_max)+"\n")

def move(motor_pin:int,angle:int)->None:
    global count
    global Angles
    Angles[motor_pin]=angle
    try:
        count=(count+1)%4
        if(count==0):
            packet = pack_data(Angles)
            client_socket.sendall(packet)
        # print(angle)
        # real_angle=pwm_val[motor_pin][0]+(pwm_val[motor_pin][1]-pwm_val[motor_pin][0])*angle/180
    except:
        if(printerror):
            print("error in changing angle")
   # print("moved motor "+str(motor_pin)+" to "+str(angle)+" degree using pulse width:"+str(int(real_angle)))
    return
