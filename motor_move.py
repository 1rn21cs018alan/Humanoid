from adafruit_servokit import ServoKit

#rewrite the move function for control of motor angle
#  this part is the only change when you shift between angle and PWM or other movement functions
kit=ServoKit(channels=16)
pwm_val=[[0,0] for i in range(16)]
printerror=False
def motor_set(motor_pin:int,pwm_min:int,pwm_max:int):
    kit.servo[motor_pin].set_pulse_width_range(pwm_min,pwm_max)
    pwm_val[motor_pin]=[pwm_min,pwm_max]
    # with open("calib_value.txt", mode="a") as file1:
    #     file1.write(str(motor_pin)+" "+str(pwm_min)+" "+str(pwm_max)+"\n")

def move(motor_pin:int,angle:int)->None:
    try:
        kit.servo[motor_pin].angle=angle
        real_angle=pwm_val[motor_pin][0]+(pwm_val[motor_pin][1]-pwm_val[motor_pin][0])*angle/180
    except:
        if(printerror):
            print("error in changing angle")
   # print("moved motor "+str(motor_pin)+" to "+str(angle)+" degree using pulse width:"+str(int(real_angle)))
    return
