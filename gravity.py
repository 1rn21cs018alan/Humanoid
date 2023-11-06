import numpy as np
import math

def angle(xy):
    val=(math.atan2(xy[1],xy[0]))*57.295
    if val<0:
        val+=360
    return val

def angle_from(origin,point):
    i,j=0,0
    if len(origin)==3:
        i=1
    if len(point)==3:
        j=1

    temp=[0]*2
    temp[0]=point[0]-origin[0]
    temp[1]=point[1+j]-origin[1+i]
    return angle(temp)

def isLeft(a, b,c,xz=0):
    return (b[0] - a[0])*(c[1+xz] - a[1+xz]) - (b[1+xz] - a[1+xz])*(c[0] - a[0]) > -0.05

def calc_dist(P,Q,x=1,y=1,z=1):
    return np.sqrt(((P[0]-Q[0])**2)*x+((P[1]-Q[1])**2)*y+((P[2]-Q[2])**2)*z)

def graham_scan(points,axis=1):
    size=len(points)
    stack=[points[0]]
    if(axis==1):
        for each in points:
            if stack[0][1]>each[1]:
                stack[0]=each
            elif stack[0][1]==each[1] and stack[0][0]>each[0]:
                stack[0]=each
        starter=stack[0]
        for i in range(size-1):
            for j in range(i,1,-1):
                if(angle_from(stack[0],points[j])>angle_from(stack[0],points[j+1])):
                    points[j],points[1+j]=points[j+1],points[j]
                else:
                    break
        stack=[[points[0],0]]
        for i in range(1,size):
            while(angle_from(stack[-1][0],points[i])<stack[-1][1]):
                stack.pop()
            stack.append([points[i],angle_from(stack[-1][0],points[i])])
        for i in range(len(stack)):
            # print(stack[i])
            stack[i]=stack[i][0]
    elif axis==2:
        for each in points:
            if stack[0][2]>each[2]:
                stack[0]=each
            elif stack[0][2]==each[2] and stack[0][0]>each[0]:
                stack[0]=each
        starter=stack[0]
        for i in range(size-1):
            for j in range(size-1-i):
                if(angle_from(stack[0],points[j])>angle_from(stack[0],points[j+1])):
                    points[j],points[1+j]=points[j+1],points[j]
        stack=[[points[0],0]]
        for i in range(1,size):
            while(angle_from(stack[-1][0],points[i])<stack[-1][1]):
                stack.pop()
            stack.append([points[i],angle_from(stack[-1][0],points[i])])
        
        for i in range(len(stack)):
            # print(stack[i])
            stack[i]=stack[i][0]
    if stack[0] is not starter:
        stack.append(starter)
    return stack


def tilt_edge(fails,point):
    min=[fails[0],((fails[0][0][0]+fails[0][1][0])/2-point[0])**2 + ((fails[0][0][2]+fails[0][1][2])/2-point[2])**2]
         
    for each in fails:
        # x=(each[0][0]+each[1][0])/2
        # y=(each[0][2]+each[1][2])/2
        dist=((each[0][0]+each[1][0])/2-point[0])**2 + ((each[0][2]+each[1][2])/2-point[2])**2
        if dist<min[1]:
            min[1]=dist
            min[0]=each

    return min[0]

def XZ_projection(p1,p2,P):
    den=math.sqrt((p2[0]-p1[0])**2 + (p2[2]-p1[2])**2)
    if den==0:
        return math.sqrt((P[0]-p1[0])**2 + (P[2]-p1[2])**2)
    return ((p2[0]-p1[0])*(p1[2]-P[2]) - (p1[0]-P[0])*(p2[2]-p1[2])) /den


class Mass_Objects:
    def __init__(self,block,weight) -> None:
        self.block=block
        self.weight=weight

    def get_center_of_mass(self):
        coords=np.zeros(3)
        for each in self.block.corner:
            coords+=each
        return coords/8



class Gravity_Environment:
    def __init__(self) -> None:
        self.moveable=[]
        self.grounded=[]
        
    def register(self,Objects,Ground_height=0,gravity=1):
        self.moveable.extend(Objects)
        self.gravity=6*gravity
        self.ground=Ground_height

    def system_COM(self):
        centre=np.zeros(3)
        mass=0.0000001
        for each in self.moveable:
            centre+=each.get_center_of_mass()*each.weight
            mass+=each.weight
            # print(each.weight)
        centre=centre/mass
        return centre        
    
    def ground_collision(self):
        min=self.moveable[0].block.corner[0][1]
        for each in self.moveable:
            for point in each.block.corner:
                if point[1]<min:
                    min=point[1]
        disp=self.ground-min
        for each in self.moveable:
            each.block.translate((0,disp,0))
        


    def detect_ground_points(self):
        self.grounded=[]
        for each in self.moveable:
            for point in each.block.corner:
                if abs(point[1]-self.ground) <0.1:
                    self.grounded.append(point)
        # print(self.grounded)
        self.grounded=graham_scan(self.grounded,axis=2)
        return self.grounded


    def is_inside(self,point):
        points=self.grounded
        size=len(points)
        if size==2:
            return [[points[0],points[1]]]
        elif size==1:
            if points[0][0]==point[0] and point[2]==points[0][2]:
                return []
            try:
                slope=(point[0]-points[0][0])/(points[0][2]-point[2])
            except ZeroDivisionError:
                slope=(point[0]-points[0][0])*1000
            new_point=[points[0][0]+1,points[0][1],points[0][2]+slope]
            return [[new_point,points[0]]]
        elif size==0:
            return []
        fails=[]
        if not isLeft(points[-1],points[0],point,xz=1):
            fails.append([points[-1],points[0]])
        # print(Val)
        for i in range(size-1):
            p1=points[i]
            p2=points[i+1]
            if not isLeft(p1,p2,point,xz=1):
                # return False
                fails.append([p1,p2])
        return fails
        # return True

    def gravitate(self):
        self.ground_collision()
        COM=self.system_COM()
        self.detect_ground_points()
        possiblitity=self.is_inside(COM)
        if possiblitity:
            p1,p2=tilt_edge(possiblitity,COM)
            d=XZ_projection(p1,p2,COM)
            # d=((p2[0]-p1[0])*(p1[2]-COM[2]) - (p1[0]-COM[0])*(p2[2]-p1[2])) / math.sqrt((p2[0]-p1[0])**2 + (p2[2]-p1[2])**2)
            # print(-d) if isLeft(p1,p2,COM) else print(d)
            # try:
            #     print("\n",(1000*p1).astype(int),(1000*p2).astype(int),(1000*COM).astype(int),d,end="")
            # except AttributeError:
            #     print("\n",np.asarray(1000*p1).astype(int),np.asarray(1000*p2).astype(int),np.asarray(1000*COM).astype(int),d,end="")

            # if isLeft(p1,p2,COM,xz=1):
            #     print("\t>!<",end="")
                # d=-d

            h=COM[1]
            magnitude=-d/np.sqrt(d**2+h**2)
            angle_radians = np.radians(magnitude*self.gravity)
            # print(angle_radians,"\t",self.angle_correction(p1,p2,d,angle_radians),"\t",angle_radians- self.angle_correction(p1,p2,d,angle_radians))
            angle_radians=self.angle_correction(p1,p2,d,angle_radians)
            # Create a vector representing the axis of rotation
            axis_vector = np.array(p2) - np.array(p1)

            # Calculate the magnitude of the axis vector
            axis_magnitude = np.linalg.norm(axis_vector)

            # Normalize the axis vector(get it's unit vector)
            try:
                normalized_axis = axis_vector / axis_magnitude
            except ZeroDivisionError:
                print("Axis Error")
                return

            # Create a rotation matrix for rotating about the normalized axis
            cos_val=np.cos(angle_radians)
            sin_val=np.sin(angle_radians)
            rotation_matrix = np.array([
                [cos_val + normalized_axis[0]**2 * (1 - cos_val), 
                normalized_axis[0] * normalized_axis[1] * (1 - cos_val) - normalized_axis[2] * sin_val,
                normalized_axis[0] * normalized_axis[2] * (1 - cos_val) + normalized_axis[1] * sin_val],
                [normalized_axis[1] * normalized_axis[0] * (1 - cos_val) + normalized_axis[2] * sin_val,
                cos_val + normalized_axis[1]**2 * (1 - cos_val),
                normalized_axis[1] * normalized_axis[2] * (1 - cos_val) - normalized_axis[0] * sin_val],
                [normalized_axis[2] * normalized_axis[0] * (1 - cos_val) - normalized_axis[1] * sin_val,
                normalized_axis[2] * normalized_axis[1] * (1 - cos_val) + normalized_axis[0] * sin_val,
                cos_val + normalized_axis[2]**2 * (1 - cos_val)]
            ])

            for each in self.moveable:
                each.block.rotate(axis_start=p1,axis_end=p2,rotation_matrix=rotation_matrix)

    def angle_correction(self,p1,p2,d,angle):
        sign=d/abs(d)
        temp=100
        sign=-1 if angle<0 else 1
        # name="None"
        for block in self.moveable:
            # print(block.block.name)
            for point in block.block.corner:
                dist=XZ_projection(p1,p2,point)
                if abs(dist)>0.4:
                    # print(dist)
                    # if not (ispositive^(dist>0 )) :
                    if True:
                        val=math.atan(point[1]/(dist))
                        if (val*sign>0) and abs(angle)>abs(sign*val):
                            angle=val
                            # temp=dist
                            # name=block.block.name
        # print(name)
        # print(name,temp,"\t",angle)
        return angle
    

