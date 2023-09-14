# DO NOT TAMPER WITH THIS PROGRAM
# modification to movement method should be done in motor_move.py
# creating new walk patterns or actions should be done in test.py or any other program that has the following
        # 1. program must contain line "import Servo_Control as SC"
        # 2. program should have a class that inherits SC.HumanoidAction to access the functions in HumanoidAction
        # 3. all the programs must be in same folder
import motor_move
from time import sleep
def delay(delay_in_seconds:float):
    sleep(delay_in_seconds/1000)



NORMAL=0
REVERSE=1

#this class stores angles of 16 motors
class Angles:
        def __init__(self,val):
                self.angle_list=[0]*16
        def get_angle(self):
                return self.angle_list
        def set_angle(self,index,value):
                self.angle_list[index]=value
#this object stores all the angles previously set in the running program
cur_angle=Angles(0)


class RoboServo ():
    def __init__(self,pinNumber:int, offset:int=0, min_thresh:int=0, max_thresh:int=180, direc:int=NORMAL):
        self.motor_init(pinNumber)

        self.offset_angle=int(offset)

        if(min_thresh>=0 & min_thresh<=180):
            self.min_angle_threshold=int(min_thresh)
        else:
            self.min_angle_threshold=int(0)

        if(max_thresh>=0 & max_thresh<=180):
            if(max_thresh>min_thresh):
                self.max_angle_threshold=int(max_thresh)
            else:
                self.max_angle_threshold=int(min_thresh)
    
        else:
            self.max_angle_threshold=int(180)
        

        self. direction = int(direc)
  
    # this functino initializes and calibrates the motors
    def motor_init(self,PCA_pin:int,pwm_min:int=566,pwm_max:int=2390)->int:
        self.Motor_pin =int(PCA_pin)
        motor_move.motor_set(PCA_pin,pwm_min,pwm_max)
        return PCA_pin
  
    # this function turns the motor to a visually accurate angle, based on standing state of robot
    # refer the motor initialization to understand effect of angles on each motor
    def turn_absolute(self, angle:int=0):
        cur_angle.set_angle(self.Motor_pin,angle)
        FinalAngle = 0 # set as 0 in case of circuit failure
        if (self.direction == NORMAL):
                FinalAngle = self.offset_angle + angle
        elif (self.direction == REVERSE):
                FinalAngle = (180 - self.offset_angle) - angle

        if (FinalAngle < self.min_angle_threshold):
                FinalAngle = self.min_angle_threshold
                if (self.direction==NORMAL):
                        cur_angle.set_angle(self.Motor_pin,FinalAngle - self.offset_angle)
                else:
                        cur_angle.set_angle(self.Motor_pin,180 - FinalAngle - self.offset_angle)
        elif (FinalAngle > self.max_angle_threshold):
                FinalAngle = self.max_angle_threshold
                if (self.direction==NORMAL):
                        cur_angle.set_angle(self.Motor_pin,FinalAngle - self.offset_angle)
                else:
                        cur_angle.set_angle(self.Motor_pin,180 - FinalAngle - self.offset_angle)
        motor_move.move(self.Motor_pin,FinalAngle)
        return self.Motor_pin,FinalAngle


# Motor initialization
Right_Shoulder_UpDown = RoboServo(0, 45, 0, 180, NORMAL)  #negative angle goes backward, positive angle turns forward(assuming shoulder UpDown is in proper orientation)
Right_Shoulder_Sideways = RoboServo(0, 0, 0, 180, NORMAL)     #positive angles only, and only in upward direction(assuming shoulder Sideways is in proper orientation)
Left_Shoulder_UpDown = RoboServo(0, 50, 0, 168, REVERSE)  #negative angle goes backward, positive angle turns forward(assuming shoulder UpDown is in proper orientation)
Left_Shoulder_Sideways = RoboServo(0, 0, 0, 180, NORMAL)      #positive angles only, and only in upward direction(assuming shoulder sideways is in proper orientation)

Right_Wrist = RoboServo(0, 97, 0, 180, REVERSE)  #positive angle means inward, negative is outward
Left_Wrist = RoboServo(0, 85, 0, 180, NORMAL)  #positive angle means inward, negative is outward

Right_Pelvis_Sideways = RoboServo(0, 20, 0, 180, REVERSE)  #positive only,represents angle the legs tilt from standing position in outward direction0,
Right_Pelvis_UpDown = RoboServo(0, 98, 0, 180, REVERSE)   # postive means bend forward, negative means bend backward
Left_Pelvis_Sideways = RoboServo(0, 2, 0, 180, NORMAL)  #positive only,represents angle the legs tilt from standing position in outward direction0,
Left_Pelvis_UpDown = RoboServo(0, 80, 0, 180, NORMAL)     # postive means bend forward, negative means bend backward

Right_Knee = RoboServo(0, 10, 70, 180, REVERSE)  # postive only, it is the angle to move backwards from standing state
Left_Knee = RoboServo(0, 0, 0, 110, NORMAL)     # postive only, it is the angle to move backwards from standing state

Right_Ankle_Sideways = RoboServo(0, 83, 0, 122, NORMAL)  #positive means bottom of foot faces outside,negative means it faces inside
Right_Ankle_UpDown = RoboServo(0, 90, 0, 135, REVERSE)    #positive means toe points upward, negative means toe points downward
Left_Ankle_Sideways = RoboServo(10, 97, 48, 180, REVERSE)  #positive means bottom of foot faces outside,negative means it faces inside
Left_Ankle_UpDown = RoboServo(0, 90, 45, 180, NORMAL)

# Class that handles actions of all 16 motors, inherit this class in future classes to reuse code
class HumanoidAction():
    def __init__(self) -> None:
        pass

  
    def init(self): # for setting up the pins on PCA9865
        Right_Shoulder_UpDown.motor_init(0)
        Right_Shoulder_Sideways.motor_init(1)
        Right_Wrist.motor_init(2)

        Left_Shoulder_UpDown.motor_init(3)
        Left_Shoulder_Sideways.motor_init(4)
        Left_Wrist.motor_init(5)

        Right_Pelvis_Sideways.motor_init(6)
        Right_Pelvis_UpDown.motor_init(7)
        Right_Knee.motor_init(8)
        Right_Ankle_UpDown.motor_init(9)
        Right_Ankle_Sideways.motor_init(10)


        Left_Pelvis_Sideways.motor_init(11)
        Left_Pelvis_UpDown.motor_init(12)
        Left_Knee.motor_init(13)
        Left_Ankle_UpDown.motor_init(14)
        Left_Ankle_Sideways.motor_init(15)
  

#************************************************************************************/
  #siting position(not recoverable)
    def sit(self) :
        Right_Shoulder_UpDown.turn_absolute(10)
        Right_Shoulder_Sideways.turn_absolute(0)
        Left_Shoulder_UpDown.turn_absolute(10)
        Left_Shoulder_Sideways.turn_absolute(0)
        Right_Wrist.turn_absolute(0)
        Left_Wrist.turn_absolute(0)
        Right_Pelvis_Sideways.turn_absolute(0)
        Right_Pelvis_UpDown.turn_absolute(90)
        Left_Pelvis_Sideways.turn_absolute(0)
        Left_Pelvis_UpDown.turn_absolute(90)
        Right_Knee.turn_absolute(0)
        Left_Knee.turn_absolute(0)
        Right_Ankle_Sideways.turn_absolute(0)
        Right_Ankle_UpDown.turn_absolute(20)
        Left_Ankle_Sideways.turn_absolute(0)
        Left_Ankle_UpDown.turn_absolute(20)
  

#************************************************************************************/

    def stand(self): #default standing position
        Right_Shoulder_UpDown.turn_absolute(0)
        Right_Shoulder_Sideways.turn_absolute(0)
        Left_Shoulder_UpDown.turn_absolute(0)
        Left_Shoulder_Sideways.turn_absolute(0)

        Right_Wrist.turn_absolute(0)
        Left_Wrist.turn_absolute(0)

        Right_Pelvis_Sideways.turn_absolute(6)
        Right_Pelvis_UpDown.turn_absolute(0)
        Left_Pelvis_Sideways.turn_absolute(6)
        Left_Pelvis_UpDown.turn_absolute(0)

        Right_Knee.turn_absolute(0)
        Left_Knee.turn_absolute(0)

        Right_Ankle_Sideways.turn_absolute(-5)
        Right_Ankle_UpDown.turn_absolute(0)
        Left_Ankle_Sideways.turn_absolute(-5)
        Left_Ankle_UpDown.turn_absolute(0)
  

#************************************************************************************/
#stable position for humanoid to stand
    def slight_squat(self):
        angle1=10
        angle2=5
        Right_Shoulder_UpDown.turn_absolute(0)
        Right_Shoulder_Sideways.turn_absolute(0)
        Left_Shoulder_UpDown.turn_absolute(0)
        Left_Shoulder_Sideways.turn_absolute(0)

        Right_Wrist.turn_absolute(0)
        Left_Wrist.turn_absolute(0)

        Right_Pelvis_Sideways.turn_absolute(angle2)
        Right_Pelvis_UpDown.turn_absolute(10)
        Left_Pelvis_Sideways.turn_absolute(angle2)
        Left_Pelvis_UpDown.turn_absolute(10)

        Right_Knee.turn_absolute(angle1+8)
        Left_Knee.turn_absolute(angle1+8)

        Right_Ankle_Sideways.turn_absolute(-angle2)
        Right_Ankle_UpDown.turn_absolute(angle1)
        Left_Ankle_Sideways.turn_absolute(-angle2)
        Left_Ankle_UpDown.turn_absolute(angle1)


#************************************************************************************/
#squats like a bird
    def squat(self,deltime:float):
        self.slight_squat()
        delay(deltime)
        Right_Shoulder_Sideways.turn_absolute(40)
        Left_Shoulder_Sideways.turn_absolute(40)

        Right_Pelvis_Sideways.turn_absolute(25)
        Right_Pelvis_UpDown.turn_absolute(60)
        Left_Pelvis_Sideways.turn_absolute(15)
        Left_Pelvis_UpDown.turn_absolute(50)

        Right_Knee.turn_absolute(60)
        Left_Knee.turn_absolute(50)

        Right_Ankle_Sideways.turn_absolute(0)
        Right_Ankle_UpDown.turn_absolute(0)
        Left_Ankle_Sideways.turn_absolute(0)
        Left_Ankle_UpDown.turn_absolute(0)
        delay(deltime)
        

#************************************************************************************/
# wont walk
    def walk(self):
        # Right_Shoulder_UpDown.turn_absolute(-15)
        # Right_Shoulder_Sideways.turn_absolute(0)
        # Left_Shoulder_UpDown.turn_absolute(15)
        # Left_Shoulder_Sideways.turn_absolute(0)
        # Right_Wrist.turn_absolute(0)
        # Left_Wrist.turn_absolute(0)
        Right_Pelvis_Sideways.turn_absolute(5)
        Right_Pelvis_UpDown.turn_absolute(40+10+5)
        Left_Pelvis_Sideways.turn_absolute(5)
        Left_Pelvis_UpDown.turn_absolute(0)
        Right_Knee.turn_absolute(45+10+5)
        Left_Knee.turn_absolute(0)
        Right_Ankle_Sideways.turn_absolute(0)
        Right_Ankle_UpDown.turn_absolute(5)
        Left_Ankle_Sideways.turn_absolute(0)
        Left_Ankle_UpDown.turn_absolute(-3)

        delay(500)

        # Right_Shoulder_UpDown.turn_absolute(15)
        # Right_Shoulder_Sideways.turn_absolute(0)
        # Left_Shoulder_UpDown.turn_absolute(-15)
        # Left_Shoulder_Sideways.turn_absolute(0)
        # Right_Wrist.turn_absolute(0)
        # Left_Wrist.turn_absolute(0)
        Right_Pelvis_Sideways.turn_absolute(5)
        Right_Pelvis_UpDown.turn_absolute(0)
        Left_Pelvis_Sideways.turn_absolute(5)
        Left_Pelvis_UpDown.turn_absolute(40+10+5)
        Right_Knee.turn_absolute(0)
        Left_Knee.turn_absolute(45+10+5)
        Right_Ankle_Sideways.turn_absolute(0)
        Right_Ankle_UpDown.turn_absolute(-3)
        Left_Ankle_Sideways.turn_absolute(0)
        Left_Ankle_UpDown.turn_absolute(5)
        delay(500)
  

#************************************************************************************/
    # turns the humanoid from one position to the other but with multiple steps in between
    # this effectively slows down the motor's motion
    def slow_action(self,initialpos:list,finalpos:list,deltime=500,steps=6):
        n=int(steps)
        for i in range(1,n+1):
            Right_Shoulder_UpDown.turn_absolute(initialpos[0] -(initialpos[0]-finalpos[0])*i/n)
            Right_Shoulder_Sideways.turn_absolute(initialpos[1] -(initialpos[1]-finalpos[1])*i/n)
            Left_Shoulder_UpDown.turn_absolute(initialpos[3] -(initialpos[3]-finalpos[3])*i/n)
            Left_Shoulder_Sideways.turn_absolute(initialpos[4] -(initialpos[4]-finalpos[4])*i/n)
            Right_Wrist.turn_absolute(initialpos[2] -(initialpos[2]-finalpos[2])*i/n)
            Left_Wrist.turn_absolute(initialpos[5] -(initialpos[5]-finalpos[5])*i/n)
            Right_Pelvis_Sideways.turn_absolute(initialpos[6] -(initialpos[6]-finalpos[6])*i/n)
            Right_Pelvis_UpDown.turn_absolute(initialpos[7] -(initialpos[7]-finalpos[7])*i/n)
            Left_Pelvis_Sideways.turn_absolute(initialpos[11] -(initialpos[11]-finalpos[11])*i/n)
            Left_Pelvis_UpDown.turn_absolute(initialpos[12] -(initialpos[12]-finalpos[12])*i/n)
            Right_Knee.turn_absolute(initialpos[8] -(initialpos[8]-finalpos[8])*i/n)
            Left_Knee.turn_absolute(initialpos[13] -(initialpos[13]-finalpos[13])*i/n)
            Right_Ankle_Sideways.turn_absolute(initialpos[10] -(initialpos[10]-finalpos[10])*i/n)
            Right_Ankle_UpDown.turn_absolute(initialpos[9] -(initialpos[9]-finalpos[9])*i/n)
            Left_Ankle_Sideways.turn_absolute(initialpos[15] -(initialpos[15]-finalpos[15])*i/n)
            Left_Ankle_UpDown.turn_absolute(initialpos[14] -(initialpos[14]-finalpos[14])*i/n)
            delay(deltime)

