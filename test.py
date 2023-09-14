import Servo_Control as SC

#rewrite this code for setting angles of robot
class RoboticMovement(SC.HumanoidAction):
    def __init__(self):
        self.init()
        return


# this is how you call the motors in this code, remember to always put "SC." before the motor name
SC.Left_Ankle_Sideways.turn_absolute(40)
