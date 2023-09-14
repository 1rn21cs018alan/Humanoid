

#rewrite the move function for control of motor angle
#  this part is the only change when you shift between angle and PWM or other movement functions
def move(motor_pin:int,angle:int)->None:
    
    print("moved motor "+str(motor_pin)+" to "+str(angle)+" degree")
    return