from Servo_Control import delay
import Servo_Control as SC
import GUI
import copy
from math import cos
def NoInterrupt():
    return False

class Humanoid_Action_Bank(SC.HumanoidAction):
    def start(self):
        self.init_2()
        self.stand()
        self.checkfunc=NoInterrupt
        self.saved_states=[[0,0,0,  0,0,0,  6,0,0,0,-5,  6,0,0,0,-5] for i in range(9)]
        self.DELangle=[0]*16
        self.walk_points=[
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -5.0, 6.0, 0.0, 0.0, 0.0, -5.0],
                            [-15, 0.0, 0.0, 25, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -17.0, 6.0, 0.0, 0.0, 0.0, 13.0],
                            [-10, 0, 0.0, 15, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -17.0, 6.0, -10.0, 0.0, 10.0, 10.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, 0.0, 6.0, -10.0, 0.0, 0.0, 0.0],
                            [30, 0.0, 0.0, -10, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, 13.0, 6.0, 0.0, 0.0, 0.0, -17.0],
                            [15, 0.0, 0.0, -15, 0.0, 0.0, 6.0, -10.0, 0.0, 10.0, 10.0, 6.0, 0.0, 0.0, 0.0, -17.0]
                        ]
        '''
        self.walk_points=[  #Squat
                            [120, 0, 0.0, 115, 0, 0.0, 6.0, 50.0, -10.0, -45.0, -5.0, 6.0, 55.0, 0.0, -45.0, -5.0],
                            [90, 0.0, 0.0, 90, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -5.0, 6.0, 0.0, 0.0, 0.0, -5.0],
                            [120, 0, 0.0, 115, 0, 0.0, 6.0, 50.0, -10.0, -45.0, -5.0, 6.0, 55.0, 0.0, -45.0, -5.0],
                            [90, 0.0, 0.0, 90, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -5.0, 6.0, 0.0, 0.0, 0.0, -5.0],
                            [120, 0, 0.0, 115, 0, 0.0, 6.0, 50.0, -10.0, -45.0, -5.0, 6.0, 55.0, 0.0, -45.0, -5.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -5.0, 6.0, 0.0, 0.0, 0.0, -5.0],
                            #Bow
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -5.0, 6.0, 0.0, 0.0, 0.0, -5.0],
                            [-45, 0.0, 0.0, -38, 0.0, 0.0, 6.0, 60, -5, -25, -5.0, 6.0, 60, 0, -30, -5.0],
                            [-15, 0.0, 0.0, -13, 0.0, 0.0, 6.0, 40, -5, -30, -5.0, 6.0, 40, 0, -30, -5.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -5.0, 6.0, 0.0, 0.0, 0.0, -5.0],
                            #Dabb
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -5.0, 6.0, 0.0, 0.0, 0.0, -5.0],
                            [80, 0.0, 83, 0.0, 125, 0.0, 6.0, 10, 0.0, 0.0, -5.0, 6.0, 10, 0.0, 0.0, -5.0],
                            [0.0, 130, 0.0, 90, 0.0, 80, 6.0, 5, 0.0, 0.0, -5.0, -2, 10, 0.0, 0.0, -5.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 10, 0.0, 0.0, -5.0, 6.0, 10, 0.0, 0.0, -5.0],
                            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.0, 0.0, 0.0, 0.0, -5.0, 6.0, 0.0, 0.0, 0.0, -5.0]
                        ]'''
                
        self.turn_points=[
                            [0,0,0,    0,0,0,    6,-10,0,0,0,      6,0,0,0,0],
                            [0,0,0,    0,0,0,    6,0,0,0,-17,    6,0,0,0,13],
                            [0,0,0,    0,0,0,    6,0,0,0,-17,    6,-10,0,10,10],
                            [0,0,0,    0,0,0,    6,0,0,0,0,      6,-10,0,0,0],
                            [0,0,0,  0,0,0,  6,0,0,0,-5,  6,0,0,0,-5],
                            [0,0,0,    0,0,0,      6,0,0,0,0,    6,-10,0,0,0],
                            [0,0,0,    0,0,0,    6,0,0,0,13,    6,0,0,0,-17],
                            [0,0,0,    0,0,0,    6,-10,0,10,10,    6,0,0,0,-17],
                            [0,0,0,    0,0,0,      6,-10,0,0,0,    6,0,0,0,0],
                            [0,0,0,  0,0,0,  6,0,0,0,-5,  6,0,0,0,-5],
            
        ]
        self.walkcount=0
        self.joystick_speed=2

    def init_2(self):
        SC.Right_Shoulder_UpDown.motor_init(0,597,2294)#done
        SC.Right_Shoulder_Sideways.motor_init(1,500,2460)#done
        SC.Right_Wrist.motor_init(2,610,2447)# done

        SC.Left_Shoulder_UpDown.motor_init(3,670,2500)#done
        SC.Left_Shoulder_Sideways.motor_init(4,500,2361)#done
        SC.Left_Wrist.motor_init(5,577,2527)#done

        SC.Right_Pelvis_Sideways.motor_init(6,1000,2500)#done
        SC.Right_Pelvis_UpDown.motor_init(7,437,2585)#done
        SC.Right_Knee.motor_init(8,566,2540)#done
        SC.Right_Ankle_UpDown.motor_init(9,662,2537)#done
        SC.Right_Ankle_Sideways.motor_init(10,625,2553)#done


        SC.Left_Pelvis_Sideways.motor_init(11,580,2390)#done
        SC.Left_Pelvis_UpDown.motor_init(12,636,2580)#done
        SC.Left_Knee.motor_init(13,566,2480)#done
        SC.Left_Ankle_UpDown.motor_init(14,626,2455)#done
        SC.Left_Ankle_Sideways.motor_init(15,616,2440)#done

    def slow_action(self,initialpos:list,finalpos:list,deltime=500,steps=6):
        n=int(steps)
        return self.sine_smoothen(initialpos,finalpos,deltime,n)
        # return self.parabolic_smoothen(initialpos,finalpos,deltime,n)
        for i in range(1,n+1):
            # <Motor> . <move to exact Degree function> ( <next step's angle calculation> )
            SC.Right_Shoulder_UpDown.turn_absolute(initialpos[0] -(initialpos[0]-finalpos[0])*i/n)
            SC.Right_Shoulder_Sideways.turn_absolute(initialpos[1] -(initialpos[1]-finalpos[1])*i/n)
            SC.Left_Shoulder_UpDown.turn_absolute(initialpos[3] -(initialpos[3]-finalpos[3])*i/n)
            SC.Left_Shoulder_Sideways.turn_absolute(initialpos[4] -(initialpos[4]-finalpos[4])*i/n)
            SC.Right_Wrist.turn_absolute(initialpos[2] -(initialpos[2]-finalpos[2])*i/n)
            SC.Left_Wrist.turn_absolute(initialpos[5] -(initialpos[5]-finalpos[5])*i/n)
            SC.Right_Pelvis_Sideways.turn_absolute(initialpos[6] -(initialpos[6]-finalpos[6])*i/n)
            SC.Right_Pelvis_UpDown.turn_absolute(initialpos[7] -(initialpos[7]-finalpos[7])*i/n)
            SC.Left_Pelvis_Sideways.turn_absolute(initialpos[11] -(initialpos[11]-finalpos[11])*i/n)
            SC.Left_Pelvis_UpDown.turn_absolute(initialpos[12] -(initialpos[12]-finalpos[12])*i/n)
            SC.Right_Knee.turn_absolute(initialpos[8] -(initialpos[8]-finalpos[8])*i/n)
            SC.Left_Knee.turn_absolute(initialpos[13] -(initialpos[13]-finalpos[13])*i/n)
            SC.Right_Ankle_Sideways.turn_absolute(initialpos[10] -(initialpos[10]-finalpos[10])*i/n)
            SC.Right_Ankle_UpDown.turn_absolute(initialpos[9] -(initialpos[9]-finalpos[9])*i/n)
            SC.Left_Ankle_Sideways.turn_absolute(initialpos[15] -(initialpos[15]-finalpos[15])*i/n)
            SC.Left_Ankle_UpDown.turn_absolute(initialpos[14] -(initialpos[14]-finalpos[14])*i/n)
            is_interrupt=(self.checkfunc())
            if is_interrupt:
                return is_interrupt
            delay(deltime)
        return False
    
    def slow(self,final_pos:list,deltime=10,steps=30):
        return self.slow_action(copy.deepcopy(SC.cur_angle.get_angle()),final_pos,deltime,steps)


    def walk(self,walking):
        stop_walk=False
        if(walking==0):
            point=[0,0,0,    0,0,0,    6,0,0,0,-5,       6,0,0,0,-5]
        elif walking==2:
            return 2
        else:
            point=[0,0,0,    0,0,0,    6,-10,0,0,0,      6,0,0,0,0]
        stop_walk=self.slow(point,steps=30)
        point=[0,0,0,    0,0,0,    6,0,0,0,-17,    6,0,0,0,13]
        if(stop_walk):
            return 2
        stop_walk=self.slow(point,steps=30)
        point=[0,0,0,    0,0,0,    6,0,0,0,-17,    6,-10,0,10,10]
        if(stop_walk):
            return 2
        stop_walk=self.slow(point,steps=30)
        point=[0,0,0,    0,0,0,    6,0,0,0,0,      6,-10,0,0,0]
        if(stop_walk):
            return 2
        stop_walk=self.slow(point,steps=30)
        point=[0,0,0,    0,0,0,    6,0,0,0,13,    6,0,0,0,-17]
        if(stop_walk):
            return 2
        stop_walk=self.slow(point,steps=30)
        point=[0,0,0,    0,0,0,    6,-10,0,10,10,     6,0,0,0,-17]
        if(stop_walk):
            return 2
        stop_walk=self.slow(point,steps=30)
        return 1
        
    def Run_Preset(self):
        while(True):
            for each in self.saved_states:
                if(self.slow(each,steps=80)):
                    return

    def set_Preset(self,pin):
        self.saved_states[pin-1]=copy.deepcopy(SC.cur_angle.get_angle())

    def load_preset(self,path):
        self.saved_states=[]
        with open(path,mode="r") as f:
            for each in f.readlines():
                if(each=="\n"):
                    continue
                angles=[0]*16
                index_angles=0
                temp=''
                for character in each:
                    if(character.isdigit() or character=='.' or character=="-" or character=="e"):
                        temp+=character
                    elif (temp!=''):
                        angles[index_angles]=float(temp)
                        index_angles+=1
                        temp=''
                self.saved_states.append(angles)

    def _front(self):
        self.walkcount=(self.walkcount+1)%len(self.walk_points)
        self.slow(self.walk_points[self.walkcount],steps=50//self.joystick_speed) #old value: steps=50 new steps=85
    def _back(self):
        self.walkcount=(self.walkcount-1)
        self.slow(self.walk_points[self.walkcount],steps=30//self.joystick_speed)
        if self.walkcount<0:
            self.walkcount=len(self.walk_points)-1
    def _left(self):
        for each in self.turn_points[:5]:
            self.slow(each,steps=20//self.joystick_speed)
    def _right(self):
        for each in self.turn_points[5:]:
            self.slow(each,steps=20//self.joystick_speed)    
    def get_SavedState(self):
        temp2=[]
        for state in self.saved_states:
            temp=[0]*16
            for i in range(16):
                temp[i]=int(state[i])
            temp2.append(temp)
        return temp2

    def parabolic_smoothen(self,initialpos:list,finalpos:list,deltime,steps):
        a=[0]*16
        for i in range(16):
            a[i]=(finalpos[i]-initialpos[i]-self.DELangle[i]*steps)/(steps*steps)
        n=steps
        for i in range(1,n+1):
            # <Motor> . <move to exact Degree function> ( <next step's angle calculation> )
            SC.Right_Shoulder_UpDown.turn_absolute  (initialpos[0]  +(self.DELangle[0]*i)   +(a[0]*i*i )  )
            SC.Right_Shoulder_Sideways.turn_absolute(initialpos[1]  +(self.DELangle[1]*i)   +(a[1]*i*i )  )
            SC.Left_Shoulder_UpDown.turn_absolute   (initialpos[3]  +(self.DELangle[3]*i)   +(a[3]*i*i )  )
            SC.Left_Shoulder_Sideways.turn_absolute (initialpos[4]  +(self.DELangle[4]*i)   +(a[4]*i*i )  )
            SC.Right_Wrist.turn_absolute            (initialpos[2]  +(self.DELangle[2]*i)   +(a[2]*i*i )  )
            SC.Left_Wrist.turn_absolute             (initialpos[5]  +(self.DELangle[5]*i)   +(a[5]*i*i )  )
            SC.Right_Pelvis_Sideways.turn_absolute  (initialpos[6]  +(self.DELangle[6]*i)   +(a[6]*i*i )  )
            SC.Right_Pelvis_UpDown.turn_absolute    (initialpos[7]  +(self.DELangle[7]*i)   +(a[7]*i*i )  )
            SC.Left_Pelvis_Sideways.turn_absolute   (initialpos[11] +(self.DELangle[11]*i)  +(a[11]*i*i)  )
            SC.Left_Pelvis_UpDown.turn_absolute     (initialpos[12] +(self.DELangle[12]*i)  +(a[12]*i*i)  )
            SC.Right_Knee.turn_absolute             (initialpos[8]  +(self.DELangle[8]*i)   +(a[8]*i*i )  )
            SC.Left_Knee.turn_absolute              (initialpos[13] +(self.DELangle[13]*i)  +(a[13]*i*i)  )
            SC.Right_Ankle_Sideways.turn_absolute   (initialpos[10] +(self.DELangle[10]*i)  +(a[10]*i*i)  )
            SC.Right_Ankle_UpDown.turn_absolute     (initialpos[9]  +(self.DELangle[9]*i)   +(a[9]*i*i )  )
            SC.Left_Ankle_Sideways.turn_absolute    (initialpos[15] +(self.DELangle[15]*i)  +(a[15]*i*i)  )
            SC.Left_Ankle_UpDown.turn_absolute      (initialpos[14] +(self.DELangle[14]*i)  +(a[14]*i*i)  )
            is_interrupt=(self.checkfunc())
            if is_interrupt:
                return is_interrupt
            delay(deltime)
        return False
    
    def sine_smoothen(self,initialpos:list,finalpos:list,deltime,steps):
        a=[0]*16
        for i in range(16):
            a[i]=finalpos[i]-initialpos[i]
        n=steps
        for i in range(1,n+1):
            factor=(1+cos(i*3.14/n))/2
            # <Motor> . <move to exact Degree function> ( <next step's angle calculation> )
            SC.Right_Shoulder_UpDown.turn_absolute  (finalpos[0]  -(a[0] *factor)  )
            SC.Right_Shoulder_Sideways.turn_absolute(finalpos[1]  -(a[1] *factor)  )
            SC.Left_Shoulder_UpDown.turn_absolute   (finalpos[3]  -(a[3] *factor)  )
            SC.Left_Shoulder_Sideways.turn_absolute (finalpos[4]  -(a[4] *factor)  )
            SC.Right_Wrist.turn_absolute            (finalpos[2]  -(a[2] *factor)  )
            SC.Left_Wrist.turn_absolute             (finalpos[5]  -(a[5] *factor)  )
            SC.Right_Pelvis_Sideways.turn_absolute  (finalpos[6]  -(a[6] *factor)  )
            SC.Right_Pelvis_UpDown.turn_absolute    (finalpos[7]  -(a[7] *factor)  )
            SC.Left_Pelvis_Sideways.turn_absolute   (finalpos[11] -(a[11]*factor)  )
            SC.Left_Pelvis_UpDown.turn_absolute     (finalpos[12] -(a[12]*factor)  )
            SC.Right_Knee.turn_absolute             (finalpos[8]  -(a[8] *factor)  )
            SC.Left_Knee.turn_absolute              (finalpos[13] -(a[13]*factor)  )
            SC.Right_Ankle_Sideways.turn_absolute   (finalpos[10] -(a[10]*factor)  )
            SC.Right_Ankle_UpDown.turn_absolute     (finalpos[9]  -(a[9] *factor)  )
            SC.Left_Ankle_Sideways.turn_absolute    (finalpos[15] -(a[15]*factor)  )
            SC.Left_Ankle_UpDown.turn_absolute      (finalpos[14] -(a[14]*factor)  )
            is_interrupt=(self.checkfunc())
            if is_interrupt:
                return is_interrupt
            delay(deltime)
        return False
        
    


class Flags:
    def init(self,stdscr):
        self.stdscr=stdscr

    def Interrupt(self):
        self.stdscr.addstr(35,0,"  interrupt check running")
        self.stdscr.timeout(1)
        key=self.stdscr.getch()
        returnedflag=False
        if(key==ord('o')):
            self.stdscr.addstr(36,0,"  interrupt detected")
            returnedflag=True
        self.stdscr.timeout(50)
        
        self.stdscr.addstr(37,0,str(returnedflag))
        return returnedflag

    def onCommand(self):
        self.stdscr.timeout(-1)
        key=self.stdscr.getch()
        if(key!=self.command_key):
            return True
        return False

    def set_Command_Key(self,key):
        self.command_key=key



flag=Flags()
