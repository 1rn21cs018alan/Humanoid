import curses
import Servo_Control as SC
from curses import wrapper # type: ignore
from time import sleep
from copy import deepcopy
import humanoid_actions

actions=None
__num_Flag={"preset_no":0}
# this function calls Servo_Control to increase  the angle of the motors
def increase(pin_num):
    angles=[]
    temp_num=0
    for i in SC.cur_angle.get_angle():
        angles.append(int(i))
        temp_num+=1
    # print((1,pin_num))
    angle_to_turn=angles[pin_num]+5 # this is the value the angle of the motor has to increase 
    if(pin_num==0):
        SC.Right_Shoulder_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==1):
        SC.Right_Shoulder_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==2):
        SC.Right_Wrist.turn_absolute(angle_to_turn)
    elif(pin_num==3):
        SC.Left_Shoulder_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==4):
        SC.Left_Shoulder_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==5):
        SC.Left_Wrist.turn_absolute(angle_to_turn)
    elif(pin_num==6):
        SC.Right_Pelvis_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==7):
        SC.Right_Pelvis_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==8):
        SC.Right_Knee.turn_absolute(angle_to_turn)
    elif(pin_num==9):
        SC.Right_Ankle_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==10):
        SC.Right_Ankle_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==11):
        SC.Left_Pelvis_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==12):
        SC.Left_Pelvis_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==13):
        SC.Left_Knee.turn_absolute(angle_to_turn)
    elif(pin_num==14):
        SC.Left_Ankle_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==15):
        SC.Left_Ankle_Sideways.turn_absolute(angle_to_turn)

    return pin_num,angle_to_turn

# this function calls Servo_Control to increase  the angle of the motors
def decrease(pin_num):
    # print((-1,pin_num))
    angles=[]
    temp_num=0
    for i in SC.cur_angle.get_angle():
        angles.append(int(i))
        temp_num+=1
    angle_to_turn=angles[pin_num]-5  # this is the value the angle of the motor has to decrease 
    if(pin_num==0):
        SC.Right_Shoulder_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==1):
        SC.Right_Shoulder_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==2):
        SC.Right_Wrist.turn_absolute(angle_to_turn)
    elif(pin_num==3):
        SC.Left_Shoulder_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==4):
        SC.Left_Shoulder_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==5):
        SC.Left_Wrist.turn_absolute(angle_to_turn)
    elif(pin_num==6):
        SC.Right_Pelvis_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==7):
        SC.Right_Pelvis_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==8):
        SC.Right_Knee.turn_absolute(angle_to_turn)
    elif(pin_num==9):
        SC.Right_Ankle_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==10):
        SC.Right_Ankle_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==11):
        SC.Left_Pelvis_Sideways.turn_absolute(angle_to_turn)
    elif(pin_num==12):
        SC.Left_Pelvis_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==13):
        SC.Left_Knee.turn_absolute(angle_to_turn)
    elif(pin_num==14):
        SC.Left_Ankle_UpDown.turn_absolute(angle_to_turn)
    elif(pin_num==15):
        SC.Left_Ankle_Sideways.turn_absolute(angle_to_turn)

    return pin_num,angle_to_turn


#this function defines the adjacency of the motors and calculates detination when attempting to change active motor
def direc(motor:int,direction:int) ->int:
    connection=[[0,1,6,3],[1,1,2,0],[1,2,6,5],
                [3,0,11,4],[4,3,5,4],[4,2,11,5],
                [0,2,7,11],[6,7,8,12],[7,8,9,13],[8,9,10,14],[9,10,10,15],
                [3,6,12,5],[11,7,13,12],[12,8,14,13],[13,9,15,14],[14,10,15,15]]
    return int(connection[motor][direction])
    """
        directions meaning
        0,1,2,3 refer to indexes of a single element in the above function
        The Value at each index equates to which motor
            to move to when navigating GUI
            
                0-UP
        3-RIGHT      1-LEFT
               2-DOWN
               
        eg: [4,3,5,4] means move to MOTOR4 when pressing up or right,
                MOTOR3 when pressing left, MOTOR5 when pressing down

        arrangement of motors(back facing camera)
            4   3   0   1
            5   |   |   2
                11  6
                12  7
                13  8
                14  9
                15  10
    """

#this is just to print out the controls
def print_control_keys(stdscr,mode=0):
    info=["X=Exit"]
    if(mode==0):
        info=[
        "X=Exit Mode/Program",
        "P=Start Walking",
        "O=Stop Walking",
        "W=Choose Motor:Up",
        "A=Choose Motor:Left",
        "S=Choose Motor:Down",
        "D=Choose Motor:Right",
        "M=Enter Joystick Mode",
        "UP/DOWN=Motor Angle",
        "0=Return to Default State",
        "N=Save Current Angles in file",
        "1~9=Set Preset",
        "L=Play Preset",
        "I=Load Presets"
        ]
    elif(mode==1):
        info=[
            "X=Exit Joystick Mode",
            "W=Move Front",
            "A=Move Left",
            "S=Move Back",
            "D=Move Right"
        ]
    elif(mode==2):
        info=[
            "LEFT/RIGHT=Navigate Options",
            "Enter=Select File",
            "L=Play Preset Positons",
            "O=Interrupt/Exit Action loop"
        ]
        
    
    screen_height,screen_width=stdscr.getmaxyx()
    x_offset=-2
    y_offset=3
    info_width=30
    for each in info:
        info_width=max(info_width,len(each))
    info_width+=5
    for each in info:
        stdscr.addstr(y_offset,x_offset+screen_width-info_width,"  "+each+(" "*(info_width-len(each))),curses.color_pair(0))
        y_offset+=1


#This function prints a white robot shape in background
def motor_bg(stdscr,mode=0):
    print_control_keys(stdscr,mode)
    spacing=3
    X_offset=30
    linespace=0
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   4   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=1
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   3   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=2
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   0   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=3
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   1   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore

    spacing+=4
    linespace=0
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   5   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=3
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   2   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore

    spacing+=4
    linespace=1
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   11  ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=2
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   6   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore

    spacing+=4
    linespace=1
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   12  ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=2
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   7   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore

    spacing+=4
    linespace=1
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   13  ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=2
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   8   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore

    spacing+=4
    linespace=1
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   14  ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=2
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   9   ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore

    spacing+=4
    linespace=1
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   15  ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    linespace=2
    stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+2,X_offset+linespace*8,"   10  ",curses.color_pair(1)) # type: ignore
    stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(1)) # type: ignore




#this function makes the motor attacked to pin number 'num' to turn cyan in GUI
# this is to show the currently selected motor
def motor_cur(stdscr,num):
    spacing=3
    X_offset=30
    if(num==4):
        linespace=0
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   4   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        return
    
    if(num==3):
        linespace=1
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   3   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
    
    if(num==0):
        linespace=2
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   0   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
    
    if(num==1):
        linespace=3
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   1   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore

    spacing+=4
    
    if(num==5):
        linespace=0
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   5   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
    
    if(num==2):
        linespace=3
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   2   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore

    spacing+=4
    
    if(num==11):
        linespace=1
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   11  ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        
    
    if(num==6):
        linespace=2
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   6   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore

    spacing+=4
    
    if(num==12):
        linespace=1
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   12  ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
    
    if(num==7):
        linespace=2
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   7   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore

    spacing+=4
    
    if(num==13):
        linespace=1
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   13  ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
    
    if(num==8):
        linespace=2
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   8   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore

    spacing+=4
    
    if(num==14):
        linespace=1
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   14  ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
    
    if(num==9):
        linespace=2
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   9   ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore

    spacing+=4
    
    if(num==15):
        linespace=1
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   15  ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
    
    if(num==10):
        linespace=2
        stdscr.addstr(spacing+1,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+2,X_offset+linespace*8,"   10  ",curses.color_pair(2)) # type: ignore
        stdscr.addstr(spacing+3,X_offset+linespace*8,"       ",curses.color_pair(2)) # type: ignore

def rect(stdscr,x1,y1,width,height,notSel=False):
    if notSel:    
        for i in range(1,height):
            stdscr.addstr(y1+i,x1+1," "*(width-2),curses.color_pair(5))
        return
    
    stdscr.addstr(y1,x1," "*width,curses.color_pair(6))
    for i in range(1,height):
        stdscr.addstr(y1+i,x1," ",curses.color_pair(6))
        stdscr.addstr(y1+i,x1+width-1," ",curses.color_pair(6))
    stdscr.addstr(y1+height,x1," "*width,curses.color_pair(6))


def preset_in_bg(stdscr,select):
    stdscr.addstr(24,67,"Selected Preset:",curses.color_pair(4))
    rect(stdscr,67+0*15,28,15,4,True)
    rect(stdscr,67+1*15,28,15,4,True)
    rect(stdscr,67+2*15,28,15,4,True)
    rect(stdscr,67+3*15,28,15,4,True)
    stdscr.addstr(30,70,"Default",curses.color_pair(5))
    stdscr.addstr(30,85,"Squat",curses.color_pair(5))
    stdscr.addstr(30,100,"Bow",curses.color_pair(5))
    stdscr.addstr(30,115,"Dab",curses.color_pair(5))
    rect(stdscr,67+select*15,28,15,4)

def select_preset_file(stdscr):
    did_choose=False
    hover_option=prev_option=0
    paths=[
        "Downloads/New/Presets.txt",
        "Downloads/New/Presets/squat.txt",
        "Downloads/New/Presets/bow.txt",
        "Downloads/New/Presets/dabb.txt"
    ]
    
    # while not did_choose:
    while(True):
        stdscr.clear()
        motor_bg(stdscr,mode=2)
        preset_in_bg(stdscr,hover_option)
        stdscr.refresh()
        curses.flushinp()
        key=stdscr.getch()
        if(key==curses.KEY_LEFT):
            prev_option=hover_option-1
        elif(key==curses.KEY_RIGHT):
            prev_option=hover_option+1
        elif(key==curses.KEY_ENTER or key==10 or key==13):
            break
        hover_option=prev_option
        if(hover_option<0):
            hover_option=0
        elif(hover_option>=len(paths)):
            hover_option=len(paths)-1
        # raise ValueError(str(hover_option))
    # stdscr.clear()
    # motor_bg(stdscr)
    actions.load_preset(paths[hover_option])
    __num_Flag['preset_no']=hover_option
    return


        


# contains the running code of GUI
def main(stdscr):
    humanoid_actions.flag.init(stdscr)
    stdscr.clear()
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_WHITE) # type: ignore
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_CYAN) # type: ignore
    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_GREEN) # type: ignore
    curses.init_pair(4,curses.COLOR_BLACK,curses.COLOR_WHITE) # type: ignore
    curses.init_pair(5,curses.COLOR_YELLOW,curses.COLOR_RED) # type: ignore
    curses.init_pair(6,curses.COLOR_YELLOW,curses.COLOR_GREEN) # type: ignore
    current_motor=4
    motor_bg(stdscr)
    motor_cur(stdscr,current_motor)
    while True :
        curses.flushinp()
        key=stdscr.getch()
        stdscr.clear()
        
        
        motor_bg(stdscr)
        if(__num_Flag['preset_no']!=0):
            preset_in_bg(stdscr,__num_Flag['preset_no'])

        sleep(0.05)


        #controls for each key press

        if key == ord('w'): # type: ignore
            current_motor=direc(current_motor,0)
        elif key == ord('s'): # type: ignore
            current_motor=direc(current_motor,2)
        elif key == ord('a'): # type: ignore
            current_motor=direc(current_motor,3)
        elif key == ord('d'):
            current_motor=direc(current_motor,1)
        elif key == curses.KEY_DOWN: # type: ignore
            strings=str(decrease(current_motor))
            stdscr.addstr(0, 0, strings+ "  ")
        elif key == curses.KEY_UP: # type: ignore
            strings=str(increase(current_motor))
            stdscr.addstr(0, 0, strings+"  ")
        elif key == ord('0'):
            setZero()
        elif key == ord('i'):
            select_preset_file(stdscr)
            # actions.load_preset("Downloads/New/Presets.txt")
        elif key == ord('n'):
            with open("Downloads/New/save_data.txt",mode="a") as f:
                f.write("\n"+str(SC.cur_angle.get_angle())+",")
            with open("Downloads/New/Presets.txt",mode="w+") as f:
                temp=actions.get_SavedState()
                for line in temp:
                    f.write("\n"+str(line))
        elif key == ord('p'):
            show_message_screen(stdscr,'walking')
        elif key == ord('x'):
            curses.endwin()
            return
        elif key>ord('0') and key<=ord('9'):
            stdscr.addstr(36, 0, " Set Preset  ")
            actions.set_Preset(key-ord('0'))
        elif key==ord('l'):
            stdscr.addstr(36, 0, " Run Preset ")
            actions.checkfunc=humanoid_actions.flag.Interrupt
            actions.Run_Preset()
            actions.checkfunc=humanoid_actions.NoInterrupt
            stdscr.timeout(-1)
        elif key==ord('m'):
            joystick_mode(stdscr)
        motor_cur(stdscr,current_motor)
        stdscr.refresh()


def show_message_screen(stdscr,message):
    global actions
    actions.checkfunc=humanoid_actions.flag.Interrupt
    walking_1=0
    stdscr.addstr(0,0,"   Walking... No input can taken until walking stops",curses.color_pair(3))
    stdscr.timeout(50)
    curses.flushinp()
    for i in range(10):
        key=stdscr.getch()
        walking_1=actions.walk(walking_1) 
        if key== ord('p'):
            break
    
    stdscr.clear()
    motor_bg(stdscr)
    stdscr.addstr(0,0,"   Walking stoped\t\t\t\t",curses.color_pair(3))
    stdscr.timeout(-1)
    actions.checkfunc=humanoid_actions.NoInterrupt
    setZero()
    return


def setZero():
    actions.slow([0,0,0, 0,0,0, 6,0,0,0,-5, 6,0,0,0,-5],steps=15)

def joystick_mode(stdscr):
    stdscr.clear()
    motor_bg(stdscr,mode=1)
    stdscr.addstr(10,60,"                            ",curses.color_pair(3))
    stdscr.addstr(11,60,"                            ",curses.color_pair(3))
    stdscr.addstr(12,60,"       Joystick Mode        ",curses.color_pair(3))
    stdscr.addstr(13,60,"                            ",curses.color_pair(3))
    stdscr.addstr(14,60,"                            ",curses.color_pair(3))
    run_flag=True
    while run_flag: 
        curses.flushinp()
        key=stdscr.getch()
        sleep(0.05)
        
        if key == ord('w'): # type: ignore
            actions._front()
        elif key == ord('s'): # type: ignore
            actions._back()
        elif key == ord('a'):
            actions._left()
        elif key == ord('d'):
            actions._right()
        elif key==ord('x'):
            actions.walkcount=0
            stdscr.clear()
            motor_bg(stdscr)
            return



# this function is to be called to start GUI Program
# Press X to stop the program
# WASD keys to change active motor(indicated in cyan)
# UP and DOWN arrow keys to increase or decrease angle of active motor
# N to save current angles of motors into a file
def start_gui(passed_actions):# passed_actions is a redundant variable, not removing it since it works as of now
    global actions
    actions=humanoid_actions.Humanoid_Action_Bank()
    actions.start()
    wrapper(main)


