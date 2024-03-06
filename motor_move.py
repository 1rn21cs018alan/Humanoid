import time
import socket
import struct
import atexit
import threading

# HOST = '192.168.1.52'
HOST = '127.0.0.1'
PORT = 22343


sending_mutex=threading.Lock()
def close_socket():
    try:
        client_socket.close()

    except Exception as e:
        return
# Function to convert the data to bytes
def pack_data(data):
    return struct.pack('!16f', *data)  # Using the struct module to format the data

def Socket_manager():
    while True:
        try:
            client_socket.connect((HOST, PORT))
            break
        except Exception:
            continue
    try:
        while True:
            with sending_mutex:
                packet = pack_data(Angles)
            
            client_socket.sendall(packet)
            time.sleep(0.02)
    except ConnectionAbortedError:
        pass
    finally:
        client_socket.close()

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Angles=[0]*16
count=0
pwm_val=[[0,0] for i in range(16)]
printerror=False
prev_pin=0
atexit.register(close_socket)
sender_thread=threading.Thread(target=Socket_manager)
sender_thread.daemon=True
sender_thread.start()


def motor_set(motor_pin:int,pwm_min:int,pwm_max:int):
    # kit.servo[motor_pin].set_pulse_width_range(pwm_min,pwm_max)
    pwm_val[motor_pin]=[pwm_min,pwm_max]
    # with open("calib_value.txt", mode="a") as file1:
    #     file1.write(str(motor_pin)+" "+str(pwm_min)+" "+str(pwm_max)+"\n")

def move(motor_pin:int,angle:int)->None:
    global count
    global Angles
    global prev_pin
    with sending_mutex:
        Angles[motor_pin]=angle
    try:
        # if(motor_pin!=prev_pin):
        #     count=(count+1)%16
        #     if(count==0):
        #         packet = pack_data(Angles)
        #         client_socket.sendall(packet)
        # else:
        #     count=0
        #     packet = pack_data(Angles)
        #     client_socket.sendall(packet)
        prev_pin=motor_pin
        # print(angle)
        # real_angle=pwm_val[motor_pin][0]+(pwm_val[motor_pin][1]-pwm_val[motor_pin][0])*angle/180
    except:
        if(printerror):
            print("error in changing angle")
   # print("moved motor "+str(motor_pin)+" to "+str(angle)+" degree using pulse width:"+str(int(real_angle)))
    return
