from Servo_Control import delay
import Servo_Control as SC
import GUI
import copy
print("Enter the motor pin as per sticker\nEnter the absolute value as is\n To enter relative angles, type r followed by the value \n somethiing like this: r13,r-5,r+10")
print("It doesn't matter whether you put + or not for relative, since it will add it to  current value regardless")
class HumanoidMovement(SC.HumanoidAction):
	def start(self):
		self.init_2()
		self.stand()

	def init_2(self):
		range_adjusting=True
		if not range_adjusting:
			SC.Right_Shoulder_UpDown.motor_init(0,566,2390)
			SC.Right_Shoulder_Sideways.motor_init(1,500,2390)
			SC.Right_Wrist.motor_init(2,566,2500)

			SC.Left_Shoulder_UpDown.motor_init(3,566,2540)
			SC.Left_Shoulder_Sideways.motor_init(4,500,2390)
			SC.Left_Wrist.motor_init(5,700,2390)

			SC.Right_Pelvis_Sideways.motor_init(6,1000,2500)
			SC.Right_Pelvis_UpDown.motor_init(7,600,2390)
			SC.Right_Knee.motor_init(8,566,2540)
			SC.Right_Ankle_UpDown.motor_init(9,850,2350)
			SC.Right_Ankle_Sideways.motor_init(10,675,2495)


			SC.Left_Pelvis_Sideways.motor_init(11,580,2390)
			SC.Left_Pelvis_UpDown.motor_init(12,700,2500)
			SC.Left_Knee.motor_init(13,566,2390)
			SC.Left_Ankle_UpDown.motor_init(14,626,2455)
			SC.Left_Ankle_Sideways.motor_init(15,616,2440)
		else:
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
	def slow(self,final_pos:list,deltime=10,steps=6):
		self.slow_action(copy.deepcopy(SC.cur_angle.get_angle()),final_pos,deltime,steps)


	def arm_lift(self,angle):
		SC.Left_Shoulder_UpDown.turn_absolute(angle)
		SC.Right_Shoulder_UpDown.turn_absolute(angle)

	def arm_flap(self,angle):
		SC.Left_Shoulder_Sideways.turn_absolute(angle)
		SC.Right_Shoulder_Sideways.turn_absolute(angle)

	def wrist_turn(self,angle):
		SC.Left_Wrist.turn_absolute(angle)
		SC.Right_Wrist.turn_absolute(angle)

	def pelvis_Splits(self,angle):
		SC.Right_Pelvis_UpDown.turn_absolute(-angle)
		SC.Left_Pelvis_UpDown.turn_absolute(angle)

	def walk2(self):
		print("start walk")
		step0=[  0,0,0,    0,25,0,   5,0,0,0,-17,    5,0,0,0,12]
		self.slow(step0,steps=50)
		print("point0")
		step1=[  0,0,0,    0,0,0,    5,0,0,0,-17,    5,0,0,0,15]
		self.slow(step1,steps=50)
		print("point1")
		# step=[  0,0,0,    0,0,0,    10,30,0,-30,-5,    0,0,0,0,15  ]
		# self.slow(step,steps=50)
		# print("point2")
		step=[  0,0,0,    0,0,0,    10,30,0,-30,-5,    0,0,0,0,15  ]
		self.slow(step,steps=50)
		print("point2")
		step3=[  0,15,0,    0,0,0,    10,20,0,-20,-5,    0,-30,0,7,13 ]
		self.slow(step3,steps=50)
		print('point3')
		# delay(1000)
		step4=[ 0,30,0,    0,0,0,    10,20,0,-20,-5,      0,-30,0,7,13]
		self.slow(step4,steps=50)
		print("point4")
		delay(1000)
		step5=[ 0,15,0,    0,0,0,    15,23,0,-30,0,      0,-25,0,7,13]
		self.slow(step5,steps=20)
		print("point5")
		# delay(1000)
		step6=[ 0,15,0,    0,0,0,    15,23,15,-30,0,      0,-25,0,7,13]
		self.slow(step6,steps=20)
		print("point6")
		delay(1000)
		step7=[ 0,15,0,    0,0,0,    15,48,15,-20,0,      0,5,10,19,0]
		self.slow(step7,steps=10)
		print("point7")
		delay(1000)
		step8=[ 0,15,0,    0,0,0,    15,40,15,-10,0,      0,5,10,19,-10]
		self.slow(step8,steps=50)
		print("point8")
		adjust_mode()

	def walk3(self):
		point1=[0,0,0,   52,0,0,   0,60,65,0,0,   0, 0, 0, 5, 0]
		self.slow(point1,steps=50)
		point2=[-30,0,0,   52,0,0,   6,35,55,17,0,    0,-15,0,45,0]
		self.slow(point2,steps=50)
		adjust_mode()
	def walk4(self,walking):
		if(walking==0):
			point=[0,0,0,	0,0,0,	6,0,0,0,-5,   	6,0,0,0,-5]
		else:
			point=[0,0,0,	0,0,0,	6,-10,0,0,0,	  6,0,0,0,0]
			
		self.slow(point,steps=30)
		point=[0,0,0,	0,0,0,	6,0,0,0,-17,	6,0,0,0,13]
		self.slow(point,steps=30)
		point=[0,0,0,	0,0,0,	6,0,0,0,-17,	6,-10,0,10,10]
		self.slow(point,steps=30)
		point=[0,0,0,	0,0,0,	6,0,0,0,0,	  6,-10,0,0,0]
		self.slow(point,steps=30)
		point=[0,0,0,	0,0,0,	6,0,0,0,13,	6,0,0,0,-17]
		self.slow(point,steps=30)
		point=[0,0,0,	0,0,0,	6,-10,0,10,10,	 6,0,0,0,-17]
		self.slow(point,steps=30)
		return 1
	def walk5(self):
		'''point=[0, 0, 0, 0, 0, 0, 5, 10, 0, 0, -10, 5, 0, 0, 0, 15]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 0, 0, 5, 40, 0, -15, -10, 5, 0, 0, 0, 15]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 0, 0, 5, 40, 0, -15, -10, 5, 0, 0, 0, 10]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 0, 0, 5, 40, 0, -20, 0, 5, 0, 0, 0, 0]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 0, 0, 5, 40, 0, -20, 5, 5, 0, 0, 0, -5]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 5, 25, -10, -20, 15, 5, -5, 30, 35, -15]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 40, 25, -10, -20, 20, 5, -5, 30, 35, -15]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 40, 25, -10, -20, 20, 5, 35, 70, 35, -20]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 40, 25, -10, -20, 20, 5, 50, 80, 35, -20]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 40, 25, -10, -20, 20, 5, 65, 95, 35, -20]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 40, 25, -10, -20, 20, 20, 65, 95, 35, -20]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 40, 25, -10, -20, 20, 20, 65, 95, 35, -20]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 40, 25, -10, -20, 20, 20, 65, 95, 50, -20]
		self.slow(point,steps=50)
		point=[0, 0, 0, 0, 85, 0, 40, 25, -10, -20, 20, 20, 65, 95, 50, -20]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 85.0, 0.0, 5, 15, -10.0, -20.0, 20.0, 20.0, 65.0, 95.0, 65, -10]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 85.0, 0.0, 5, 15, -10.0, -20, 20, 20.0, 65.0, 95.0, 45, -25]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 85.0, 0.0, 5, 15, -10.0, -20, 20, 20.0, 75, 105, 45, -25]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 85.0, 0.0, 5, 15, -10.0, -20, 20, 20.0, 75, 105, 45, -25]
		self.slow(point,steps=50)
		point=[70, 0.0, 0.0, -38, 15, 0.0, 5, 15, -10.0, -20, 20, 20.0, 75, 105, 45, -25]
		self.slow(point,steps=50)
		point=[70, 0.0, 0.0, -38, 15, 0.0, 5, 15, -10.0, -20, 20, 20.0, 75, 75, 45, -25]
		self.slow(point,steps=50)
		point=[70, 0.0, 0.0, 12, 15, 0.0, 5, 15, -10.0, -20, 20, 20.0, 75, 75, 45, -25]
		self.slow(point,steps=50)
		point=[0, 0.0, 0.0, 12, 15, 0.0, 5, 15, -10.0, -20, 20, 20.0, 75, 75, 45, -25]
		self.slow(point,steps=50)
		point=[0, 0.0, 0.0, 12, 15, 0.0, 5, 15, -10.0, -20, 20, 20.0, 75, 35, 5, -25]
		self.slow(point,steps=50)
		point=[65, 0.0, 0.0, -38, 15, 0.0, 5, 15, -10.0, -20, 20, 20.0, 75, 35, 5, -25]
		self.slow(point,steps=50)
		point=[65, 0.0, 0.0, -38, 15, 0.0, 5, 15, -10.0, -15, 20, 20.0, 95, 35, 5, -25]
		self.slow(point,steps=50)
		point=[65, 0.0, 0.0, -38, 15, 0.0, 5, 15, -10, -25, 20, 20.0, 95, 45, 5, -25]
		self.slow(point,steps=50)
		point=[65, 0.0, 0.0, -38, 15, 0.0, 5, 10, -10, 0, 15, 20.0, 80, 45, -25, -10]
		self.slow(point,steps=50)
		point=[65, 0.0, 0.0, -38, 15, 0.0, 5, 10, -10, 0, 15, 20.0, 80, 45, 15, -10]
		self.slow(point,steps=50)
		point=[65, 0.0, 0.0, -38, 15, 0.0, 5, 10, -10, 0, 0, 20.0, 80, 45, 15, 0]
		self.slow(point,steps=50)
		point=[15, 0.0, 0.0, -8, 15, 0.0, 5, 10, -10, 0, 0, 20.0, 80, 45, 15, 0]
		self.slow(point,steps=50)
		point=[15, 0.0, 0.0, -8, 15, 0.0, 5, -10, -10, 0, 0, 20.0, 40, 45, 15, 0]
		self.slow(point,steps=50)
		point=[15, 0.0, 0.0, -8, 15, 0.0, 5, -10, -10, 0, 10, 20.0, 40, 45, 15, 5]
		self.slow(point,steps=50)
		point=[15, 0.0, 0.0, -8, 15, 0.0, 5, -10, -10, 0, 10, 20.0, 40, 45, 15, 5]
		self.slow(point,steps=50)
		point=[15, 0.0, 0.0, -8, 15, 0.0, 5, -10, -10, 0, 10, 20.0, 40, 45, 15, 5]
		self.slow(point,steps=50)'''
		'''point=[0, 0, 0, 0, 0, 0, 5, 0, 0, 0, -5, 5, 0, 0, 0, -5]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5, 30, 30, 10, -10, 5, 0.0, 0, 10, 10]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5, 30, 30, 10, -5, 5, 0.0, 0, 10, -5]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5, 0.0, 0, 10, 10, 5, 30, 30, 10, -10]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5, 0, 0, 10, -5, 5, 30, 30, 10, -5]
		self.slow(point,steps=50)'''
		#self.slow(point,steps=50)
		'''point=[0.0, 0.0, 0.0, -5, 0, 0.0, 0.0, 30, 30, 0.0, 10, 0.0, 0.0, 0.0, 0.0, 15]
		self.slow(point,steps=50)
		point=[0.0, 60, 0.0, -5, 0, 0.0, 15, 30, 30, 0.0, -5, 15, 0.0, 0.0, 0.0, 15]
		self.slow(point,steps=50)
		point=[-45, 0, 0.0, -5, 0, 0.0, 15, 35, 30, 0.0, -5, 15, 0.0, 0.0, 5, 15]
		
		self.slow(point,steps=50)
		point=[-45, 0, 0.0, -5, 0, 0.0, 15, 45, 40, 15, -20, 15, 0.0, 0.0, 5, 15]
		self.slow(point,steps=50)
		point=[10, 80, 0.0, -5, 0, 0.0, 15, 75, 70, 15, -20, 15, 0.0, 0.0, 5, 15]
		self.slow(point,steps=50)
		point=[10, 80, 0.0, -38, 0, 0.0, 15, 75, 70, 15, -20, 15, -5, 5, 5, 15]
		self.slow(point,steps=50)
		point=[10, 80, 0.0, -38, 0, 0.0, 15, 75, 70, 15, -20, 15, -25, 5, 5, 15]
		self.slow(point,steps=50)
		point=[-20, 30, 0.0, -38, 0, 0.0, 15, 65, 55, 15, -20, 15, -25, 5, 5, 15]
		self.slow(point,steps=50)
		point=[-20, 30, 0.0, -38, 0, 0.0, 10, 30, 25, 15, -20, 10, -25, 5, 5, 15]
		self.slow(point,steps=50)
		point=[-20, 30, 0.0, -38, 0, 0.0, 10, 30, 25, 10, -15, 10, -25, 0, 10, 15]
		self.slow(point,steps=50)
		point=[-20, 30, 0.0, -38, 0, 0.0, 10, 30, 25, 10, 0, 10, -25, 0, 10, 10]
		self.slow(point,steps=50)
		point=[-20, 30, 0.0, -38, 0, 0.0, 10, 30, 25, 5, -5, 10, -25, 0, 10, 10]
		self.slow(point,steps=50)
		point=[-20, 30, 0.0, -38, 0, 0.0, 10, 30, 25, 5, -5, 10, -25, 0, 10, 0]
		self.slow(point,steps=50)
		point=[0, 0, 0.0, 2, 0, 0.0, 10, 30, 25, 5, 10, 10, -25, 0, 10, 10]
		self.slow(point,steps=50)
		point=[0, 0, 0.0, 2, 0, 0.0, 10, 0, 0, 0, 0, 10, 0, 0, 0, 0]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]'''
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5, 30, 30, 10, -15, 5, 0.0, 0, 10, 15]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5, 30, 30, 10, -5, 5, 0.0, 0, 10, -5]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5, 0.0, 0, 10, 15, 5, 30, 30, 10, -15]
		self.slow(point,steps=50)
		point=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5, 0, 0, 10, -5, 5, 30, 30, 10, -5]
		self.slow(point,steps=50)

	def walk6(self):
		point=[0, 0, 0, 0, 0, 0, 5, 0, 0, 0, -5, 5, 0, 0, 0, -5]
		self.slow(point,steps=50)
		
		
		

def adjust_mode():
	minor_adjust_flag=True
	while minor_adjust_flag:
		angles=[]
		temp_num=0
		for i in SC.cur_angle.get_angle():
			angles.append((temp_num,int(i)))
			temp_num+=1
		print(angles)
		#print([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
		pin_num=2
		try:
			pin_string=(input("Enter Pin number:"))
			if(pin_string.strip()=="@s"):
				with open("save_data.txt",mode="a") as f:
					f.write("\n"+str(angles))
				continue
			elif(pin_string.strip()=="@0"):
				actions.slow([0,0,0,   0,0,0,   0,0,0,0,0,   0,0,0,0,0],steps=50)
				continue
			pin_num=int(pin_string)
		except ValueError:
			print("Invalid Number")
			continue
		pin_num=2 if (pin_num<0 or pin_num>15) else pin_num
		print("previous angle:"+str(angles[pin_num][1]))
		angle_to_turn=(input("Enter Angle:")).strip()
		try:
			if(angle_to_turn[0]=='r'):
				angle_to_turn=int(angle_to_turn[1:])+angles[pin_num][1]
			else:
				angle_to_turn=int(angle_to_turn)
		except ValueError:
			print("Invalid Number")
			continue
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


actions=HumanoidMovement()
actions.start()
delay(1000)

mode=12
if mode==1:
	actions.arm_lift(90)
	delay(2000)
elif mode==2:
	actions.arm_flap(90)
	delay(2000)
elif mode==3:
	actions.arm_flap(90)
	delay(700)
	actions.wrist_turn(90)
elif mode==4:
	delay(1000)
	actions.pelvis_Splits(90)
elif mode==5:
	actions.slow_action([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,90,0,0,90,0,60,0,0,0,0,60,0,0,0,0],deltime=100,steps=30)
	delay(5000)
	actions.slow_action([0,90,0,0,90,0,60,0,0,0,0,60,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],deltime=100,steps=30)
elif mode==6:
	SC.Right_Knee.turn_absolute(90)
	SC.Left_Knee.turn_absolute(90)

elif mode==7:
	delay(700)

	SC.Right_Shoulder_UpDown.turn_absolute(0)
	SC.Right_Shoulder_Sideways.turn_absolute(0)
	SC.Right_Wrist.turn_absolute(0)

	SC.Left_Shoulder_UpDown.turn_absolute(0)
	SC.Left_Shoulder_Sideways.turn_absolute(0)
	SC.Left_Wrist.turn_absolute(0)

	SC.Right_Pelvis_Sideways.turn_absolute(5)
	SC.Right_Pelvis_UpDown.turn_absolute(0)
	SC.Right_Knee.turn_absolute(0)
	SC.Right_Ankle_UpDown.turn_absolute(0)
	SC.Right_Ankle_Sideways.turn_absolute(-5)

	SC.Left_Pelvis_Sideways.turn_absolute(5)
	SC.Left_Pelvis_UpDown.turn_absolute(0)
	SC.Left_Knee.turn_absolute(0)
	SC.Left_Ankle_UpDown.turn_absolute(0)
	SC.Left_Ankle_Sideways.turn_absolute(-5)

	adjust_mode()
	
	########[  0,0,0,    0,0,0,    5,40,30,-20,-5,    5,0,0,0,-5  ]


	#[  0,0,0,    0,0,0,    5,40,30,-20,-5,    5,0  ,0,0 ,-5     ]
	#[  0,0,0,    0,0,0,    5,40,30,-10,-5,    5,-30,0,30,-5  ]
	#[  0,0,0,    0,0,0,    5,0,0,-10,-5,      5,60,40,-30,-5     ]
	#[  0,0,0,    0,0,0,    5,0,0,-10,-5,      5,60,90,-30,-5     ]


	#[  0,0,0,    0,0,0,    5,0 ,0 ,-10,-5,    5,40,40,0,-5   ]

elif mode==8:
	flag_here=True
	while flag_here:
		for i in range(3):
			actions.walk()
		flag_here=bool(input("redo?"))
elif mode==9:
	delay(1000)
	for i in range(1):
		actions.walk2()
elif mode==10:
	while True:
		substep=int(input("substep?"))
		if(substep<=3 or substep==13):
			step6=[ 0,15,0,    0,0,0,    15,23,15,-30,0,      0,-25,0,7,13]
			actions.slow(step6,steps=20)
			print("point6")
			delay(1000)
		if(substep<=2 or substep==12):
			step7=[ 0,15,0,    0,0,0,    15,48,15,-20,0,      0,5,10,19,0]
			actions.slow(step7,deltime=100,steps=50)
			print("point7")
			delay(1000)
		if(substep<=1 or substep==11):
			step8=[ 0,15,0,    0,0,0,    15,40,15,-10,0,      0,5,10,19,-10]
			actions.slow(step8,steps=50)
			print("point8")
elif mode == 11:
	walking=0
	for i in range(15):
		walking=actions.walk4(walking)
	adjust_mode()
elif mode==12:
	#actions.walk6()
	for i in range(0):
		actions.walk5()
		#actions.walk6()
	# adjust_mode()
	GUI.start_gui(actions)
	
print(SC.cur_angle.get_angle())
