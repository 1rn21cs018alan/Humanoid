from Servo_Control import delay
import Servo_Control as SC
import GUI
import copy

def NoInterrupt():
    return False

class Humanoid_Action_Bank(SC.HumanoidAction):
    def start(self):
        self.init_2()
        self.stand()
        self.checkfunc=NoInterrupt
        self.saved_states=[[0,0,0,  0,0,0,  6,0,0,0,-5,  6,0,0,0,-5] for i in range(9)]
        self.walk_points=[
                            [0,0,0,    0,0,0,    6,-10,0,0,0,      6,0,0,0,0],
                            [0,0,0,    0,0,0,    6,0,0,0,-17,    6,0,0,0,13],
                            [0,0,0,    0,0,0,    6,0,0,0,-17,    6,-10,0,10,10],
                            [0,0,0,    0,0,0,    6,0,0,0,0,      6,-10,0,0,0],
                            [0,0,0,    0,0,0,    6,0,0,0,13,    6,0,0,0,-17],
                            [0,0,0,    0,0,0,    6,-10,0,10,10,     6,0,0,0,-17]
                        ]
        self.walkcount=0

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
        n=steps
        for i in range(1,n+1):
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
        for each in self.saved_states:
            if(self.slow(each)):
                return

    def set_Preset(self,pin):
        self.saved_states[pin-1]=copy.deepcopy(SC.cur_angle.get_angle())

    def _front(self):
        self.slow(self.walk_points[self.walkcount])
        self.walkcount=(self.walkcount+1)%len(self.walk_points)
    def _back(self):
        self.slow(self.walk_points[self.walkcount])
        self.walkcount=(self.walkcount-1)
        if self.walkcount<0:
            self.walkcount=len(self.walk_points)-1
    


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