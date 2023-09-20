from OpenGL.GLUT import *  
from OpenGL.GL import *  
from OpenGL.GLU import *  
import pygame
from time import sleep
from pygame.locals import *
import math
import numpy as np
from __constants import *
from copy import deepcopy as dc
import socket
import struct

def unpack_data(packet):
    return struct.unpack('!16f', packet)

HOST = '127.0.0.1'  # Use localhost
PORT = 22343  # Choose the same port number as your sender program

disable_Sticky=True


def Stick_to_ground():
    global Blocks
    vert1=np.array(Blocks[Left_Foot].corner)
    vert2=np.array(Blocks[Right_Foot].corner)
    # Calculate the normal vectors and plane equations for vert1 and vert2
    normal1 = np.cross(vert1[1] - vert1[0], vert1[4] - vert1[0])
    normal1 /= np.linalg.norm(normal1)
    a1, b1, c1 = normal1
    d1 = -np.dot(normal1, vert1[0])

    normal2 = np.cross(vert2[1] - vert2[0], vert2[4] - vert2[0])
    normal2 /= np.linalg.norm(normal2)
    a2, b2, c2 = normal2
    d2 = -np.dot(normal2, vert2[0])

    # Count points below vert1 and vert2
    points_below_vert1 = 0
    points_below_vert2 = 0
    points_considered=[]
    for each in Blocks:
        points_considered.extend(each.corner)
    for point in points_considered:
        distance1 = a1 * point[0] + b1 * point[1] + c1 * point[2] + d1
        distance2 = a2 * point[0] + b2 * point[1] + c2 * point[2] + d2

        if distance1 < 0:
            points_below_vert1 += 1
        if distance2 < 0:
            points_below_vert2 += 1

    if( points_below_vert1 <= points_below_vert2):
        point1 = vert1[1]
        point0 = vert1[0]
        point4 = vert1[4]
    else:
        point1 = vert2[1]
        point0 = vert2[0]
        point4 = vert2[4]

    # Calculate vectors from point0 to point1 and from point0 to point4
    vector1_0 = point1 - point0
    vector4_0 = point4 - point0

    # Calculate the normal vector of the plane defined by points 1, 0, and 4
    normal_vector = np.cross(vector1_0, vector4_0)
    
    # Normalize the normal vector
    normal_vector /= np.linalg.norm(normal_vector)

    # Find the rotation matrix to align the normal vector with the positive Y-axis (y=0 plane)
    target_vector = np.array([0, 1, 0])  # Positive Y-axis
    rotation_axis = np.cross(normal_vector, target_vector)
    rotation_angle = np.arccos(np.dot(normal_vector, target_vector))
    
    # Create the rotation matrix
    c = np.cos(rotation_angle)
    s = np.sin(rotation_angle)
    t = 1 - c
    x, y, z = rotation_axis
    rotation_matrix = np.array([
        [t * x * x + c, t * x * y - z * s, t * x * z + y * s],
        [t * x * y + z * s, t * y * y + c, t * y * z - x * s],
        [t * x * z - y * s, t * y * z + x * s, t * z * z + c]
    ])
    trs=np.dot(np.array(point0), rotation_matrix.T)
    trs2=np.dot(np.array(point1), rotation_matrix.T)
    dist=np.sqrt(np.sum((trs-trs2)**2))
    # print(dist,Blocks[Left_Foot].depth)
    ratio=Blocks[Left_Foot].depth/dist
    ratio=1
    trs[0]=trs[2]=0
    # print(trs)
    # Apply the rotation matrix to all points on the surface
    if(abs(ratio-1)<0.005):
        for i in range(len(Blocks)):
            Blocks[i].corner=list(np.dot(np.array(Blocks[i].corner), rotation_matrix.T)-trs)
    else:
        for i in range(len(Blocks)):
            Blocks[i].corner=list((np.dot(np.array(Blocks[i].corner), rotation_matrix.T)-trs)*ratio)


def sin(val):
    return math.sin(val*0.01745)
def cos(val):
    return math.cos(val*0.01745)

colors={'red':(1,0,0,1),
        'green':(0,1,0,1),
        'yellow':(1,1,0,1),
        'dark green':(0,0.5,0,1),
        'light green':(0.5,1,0.5,1),
        'blue':(0,0,1,1),
        'dark blue':(0,0,0.5,1),
        'light blue':(0.5,0.5,1,1),
        "white":(1,1,1,1),
        "grey":(0.5,0.5,0.5,1),
        "light grey":(0.75,0.75,0.75,1),
        "dark gray":(0.3,0.3,0.3,1)}

class CuboidBlock:
    def __init__(self,Height,Width,Depth,color=colors['light grey']):
        self.corner=[]
        self.height=Height
        self.width=Width
        self.depth=Depth
        self.color=color
        h=Height/2
        w=Width/2
        d=Depth/2
        for i in (-1,1):
            for j in (-1,1):
                for k in (-1,1):
                    self.corner.append([i*h,j*w,d*k])
        
        self.edges=(
            (0,1),
            (0,2),
            (1,3),
            (2,3),
            (0,4),
            (1,5),
            (2,6),
            (3,7),
            (4,5),
            (4,6),
            (5,7),
            (6,7),

            )

        self.surfaces=(
            (0,1,3,2),
            (4,5,7,6),
            (0,1,5,4),
            (2,3,7,6),
            (1,3,7,5),
            (2,0,4,6),
        )
        self.pos={'x':0,'y':0}
    
    def draw_edge(self,coords=(0,0,0)):
        glBegin(GL_LINES)
        current_color=list(colors['red'])
        glColor4fv(current_color)
        for edge in self.edges:
            for vertex in edge:
                self.corner[vertex]
                point=(self.corner[vertex][0]+coords[0], self.corner[vertex][1]+coords[1],self.corner[vertex][2]+coords[2])
                glVertex3fv(point)
        glColor3fv((0,0,0))
        glEnd()
    
    def draw_surface(self,coords=(0,0,0)):
        glBegin(GL_QUADS)
        current_color=list(self.color)
        change=0.05
        if(current_color==[1,1,1,1]):
            change=-0.05
        for i in range(len(self.surfaces)):
            surface=self.surfaces[i]
            glColor4fv(current_color)
            for vertex in surface:
                self.corner[vertex]
                point=(self.corner[vertex][0]+coords[0], self.corner[vertex][1]+coords[1],self.corner[vertex][2]+coords[2])
                glVertex3fv(point)
            current_color[0]+=change
            current_color[1]+=change
            current_color[2]+=change
        glColor3fv((0,0,0))
        glEnd()


class FreeBlock(CuboidBlock):
    def __init__(self, Height, Width, Depth, color=colors['light grey'],loc=[0,0,0]):
        super().__init__(Height, Width, Depth, color)
        self.dimensions=dc(self.corner)
        self.reset_to_coords(loc)

    def draw(self):
        self.draw_surface()
        self.draw_edge()
    
    def reset_to_coords(self,coords):
        for i in range(len(self.corner)):
            self.corner[i][0]=self.dimensions[i][0]+coords[0]
            self.corner[i][1]=self.dimensions[i][1]+coords[1]
            self.corner[i][2]=self.dimensions[i][2]+coords[2]
    
    
    def translate(self,coords):
        for i in range(len(self.corner)):
            self.corner[i][0]+=coords[0]
            self.corner[i][1]+=coords[1]
            self.corner[i][2]+=coords[2]
    
    def rotate(self, axis_start=[0,0,0], axis_end=[0,1,0], angle_degrees=1):
        # Convert angle to radians
        angle_radians = np.radians(angle_degrees)

        # Create a vector representing the axis of rotation
        axis_vector = np.array(axis_end) - np.array(axis_start)

        # Calculate the magnitude of the axis vector
        axis_magnitude = np.linalg.norm(axis_vector)

        # Normalize the axis vector(get it's unit vector)
        try:
            normalized_axis = axis_vector / axis_magnitude
        except ZeroDivisionError:
            print("Axis Error")
            return

        # Create a rotation matrix for rotating about the normalized axis
        rotation_matrix = np.array([
            [np.cos(angle_radians) + normalized_axis[0]**2 * (1 - np.cos(angle_radians)), 
            normalized_axis[0] * normalized_axis[1] * (1 - np.cos(angle_radians)) - normalized_axis[2] * np.sin(angle_radians),
            normalized_axis[0] * normalized_axis[2] * (1 - np.cos(angle_radians)) + normalized_axis[1] * np.sin(angle_radians)],
            [normalized_axis[1] * normalized_axis[0] * (1 - np.cos(angle_radians)) + normalized_axis[2] * np.sin(angle_radians),
            np.cos(angle_radians) + normalized_axis[1]**2 * (1 - np.cos(angle_radians)),
            normalized_axis[1] * normalized_axis[2] * (1 - np.cos(angle_radians)) - normalized_axis[0] * np.sin(angle_radians)],
            [normalized_axis[2] * normalized_axis[0] * (1 - np.cos(angle_radians)) - normalized_axis[1] * np.sin(angle_radians),
            normalized_axis[2] * normalized_axis[1] * (1 - np.cos(angle_radians)) + normalized_axis[0] * np.sin(angle_radians),
            np.cos(angle_radians) + normalized_axis[2]**2 * (1 - np.cos(angle_radians))]
        ])

        # Translate the point to the origin (subtract axis_start), Rotate the translated point and undo translation
        for i in range(len(self.corner)):
            translated_point = np.array(self.corner[i]) - np.array(axis_start)
            self.corner[i]= np.dot(rotation_matrix, translated_point)+ np.array(axis_start)


class Motor:
    def __init__(self,i,Block,latch_verticies,offset,default_angle=0) -> None:
        self.mot=i
        self.block=Block
        self.latch_vertex=latch_verticies
        self.offset=offset
        self.cur_angle=default_angle
    def turn_what(self,mot):
        if(mot==   Right_Shoulder_UpDown):
            return[  Right_Shoulder,Right_Elbow,Right_Wrist]
        elif(mot== Right_Shoulder_Sideways):
            return[  Right_Elbow,Right_Wrist ]
        elif(mot== Left_Shoulder_UpDown):
            return[  Left_Shoulder,Left_Elbow,Left_Wrist]
        elif(mot== Left_Shoulder_Sideways):
            return[  Left_Elbow,Left_Wrist]
        elif(mot== Right_Wrist):
            return[  Right_Wrist]
        elif(mot== Left_Wrist):
            return[  Left_Wrist]
        elif(mot== Right_Pelvis_Sideways):
            return[  Right_Pelvis,Right_Thigh,Right_Calf,Right_Ankle,Right_Foot ]
        elif(mot== Right_Pelvis_UpDown):
            return[  Right_Thigh,Right_Calf,Right_Ankle,Right_Foot ]
        elif(mot== Right_Knee):
            return[  Right_Calf,Right_Ankle,Right_Foot ]
        elif(mot== Right_Ankle_UpDown):
            return[  Right_Ankle,Right_Foot ]
        elif(mot== Right_Ankle_Sideways):
            return[  Right_Foot ]
        elif(mot== Left_Pelvis_Sideways):
            return[  Left_Pelvis,Left_Thigh,Left_Calf,Left_Ankle,Left_Foot]
        elif(mot== Left_Pelvis_UpDown):
            return[  Left_Thigh,Left_Calf,Left_Ankle,Left_Foot]
        elif(mot== Left_Knee):
            return[  Left_Calf,Left_Ankle,Left_Foot]
        elif(mot== Left_Ankle_UpDown):
            return[  Left_Ankle,Left_Foot]
        elif(mot== Left_Ankle_Sideways):
            return[  Left_Foot]
        return Head
    
    def rotate(self,angle):
        Block=self.block
        latch_verticies=self.latch_vertex
        offset=self.offset
        p1=Block.corner[latch_verticies[0]]
        p2=Block.corner[latch_verticies[1]]
        p3=Block.corner[latch_verticies[2]]
        p4=Block.corner[latch_verticies[3]]
        point1=[0]*3
        point2=[0]*3
        for j in range(3):
            point1[j]=((p1[j]-p2[j])*offset)+(p1[j]+p2[j])/2
            point2[j]=((p3[j]-p4[j])*offset)+(p3[j]+p4[j])/2
        if(abs(angle-self.cur_angle)<0.5):
            return
        motors_to_turn=self.turn_what(self.mot)
        for each in motors_to_turn:
            Blocks[each].rotate(axis_start=point1,axis_end=point2,angle_degrees=angle-self.cur_angle)
        self.cur_angle=angle




def main():
    global Motors
    global Blocks
    pygame.init()
    display = (1200,800)
    displayCenter=(display[0]/2,display[1]/2)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    gluPerspective(65, (display[0]/display[1]), 0.1, 70.0)
    view_angle=0
    glTranslatef(0,-10,-25)
    Hold_Shift=False



    Blocks[Head]=FreeBlock(1,1,1,loc=[0,15.5,0],color=colors['yellow'])
    Blocks[Torso]=FreeBlock(4.2,4.2,1,loc=[0,12.8,0])
    
    Blocks[Right_Shoulder]=FreeBlock(1,1.6,1.6,loc=[-2.7,14.6,0],color=colors['dark blue'])
    Blocks[Left_Shoulder] =FreeBlock(1,1.6,1.6,loc=[ 2.7,14.6,0],color=colors['dark blue'])

    Blocks[Right_Elbow]=FreeBlock(1,4.2,1.6,loc=[-3.7,12.8,0],color=colors['blue'])
    Blocks[Left_Elbow] =FreeBlock(1,4.2,1.6,loc=[ 3.7,12.8,0],color=colors['blue'])
    
    Blocks[Right_Wrist]=FreeBlock(1,2.1,1.6,loc=[-3.7,9.65,0],color=colors['light blue'])
    Blocks[Left_Wrist] =FreeBlock(1,2.1,1.6,loc=[ 3.7,9.65,0],color=colors['light blue'])
    
    Blocks[Right_Pelvis]=FreeBlock(1.6,2.5,1,loc=[-1.3,9.45,0],color=colors['red'])
    Blocks[Left_Pelvis] =FreeBlock(1.6,2.5,1,loc=[ 1.3,9.45,0],color=colors['red'])

    Blocks[Right_Thigh]=FreeBlock(1.6,3.2,1,loc=[-1.3,6.6,0],color=colors['grey'])
    Blocks[Left_Thigh] =FreeBlock(1.6,3.2,1,loc=[ 1.3,6.6,0],color=colors['grey'])

    Blocks[Right_Calf]=FreeBlock(1.6,2.6,1,loc=[-1.3,3.7,0],color=colors['dark gray'])
    Blocks[Left_Calf] =FreeBlock(1.6,2.6,1,loc=[ 1.3,3.7,0],color=colors['dark gray'])

    Blocks[Right_Ankle]=FreeBlock(1.6,1.9,1,loc=[-1.3,1.45,0],color=colors['green'])
    Blocks[Left_Ankle] =FreeBlock(1.6,1.9,1,loc=[ 1.3,1.45,0],color=colors['green'])

    Blocks[Right_Foot]=FreeBlock(3.3,0.5,4,loc=[-1.95, 0.25, 0.5],color=colors['light green'])
    Blocks[Left_Foot] =FreeBlock(3.3,0.5,4,loc=[ 1.95, 0.25, 0.5],color=colors['light green'])

    Motors[Right_Shoulder_UpDown] =    Motor(Right_Shoulder_UpDown   ,Blocks[Right_Shoulder],[ 5,  6, 1, 2 ],0               ,45         )#done
    Motors[Right_Shoulder_Sideways] =  Motor(Right_Shoulder_Sideways ,Blocks[Right_Elbow   ],[ 7 , 7, 6, 6 ],0               ,0          )#done
    Motors[Left_Shoulder_UpDown] =     Motor(Left_Shoulder_UpDown    ,Blocks[Left_Shoulder ],[ 1 , 2, 5, 6 ],0               ,130        )#done
    Motors[Left_Shoulder_Sideways] =   Motor(Left_Shoulder_Sideways  ,Blocks[Left_Elbow    ],[ 2 , 2, 3, 3 ],0               ,0          )#done
    Motors[Right_Wrist] =              Motor(Right_Wrist             ,Blocks[Right_Wrist   ],[ 3 , 7, 2, 6 ],0               ,83         )
    Motors[Left_Wrist] =               Motor(Left_Wrist              ,Blocks[Left_Wrist    ],[ 3 , 7, 2, 6 ],0               ,85         )
    Motors[Right_Pelvis_Sideways] =    Motor(Right_Pelvis_Sideways   ,Blocks[Right_Pelvis  ],[ 2 , 6, 3, 7 ],0               ,154        )
    Motors[Right_Pelvis_UpDown] =      Motor(Right_Pelvis_UpDown     ,Blocks[Right_Thigh   ],[ 2 , 3, 6 ,7 ],0               ,82         )
    Motors[Left_Pelvis_Sideways] =     Motor(Left_Pelvis_Sideways    ,Blocks[Left_Pelvis   ],[ 2 , 6, 3, 7 ],0               ,8          )
    Motors[Left_Pelvis_UpDown] =       Motor(Left_Pelvis_UpDown      ,Blocks[Left_Thigh    ],[ 6 , 7, 2 ,3 ],0               ,80         )
    Motors[Right_Knee] =               Motor(Right_Knee              ,Blocks[Right_Calf    ],[ 6 , 7, 2 ,3 ],0               ,170        )
    Motors[Left_Knee] =                Motor(Left_Knee               ,Blocks[Left_Calf     ],[ 2 , 3, 6 ,7 ],0               ,0          )
    Motors[Right_Ankle_Sideways] =     Motor(Right_Ankle_Sideways    ,Blocks[Right_Foot    ],[ 3 , 7, 2, 6 ],-0.22           ,78         )
    Motors[Right_Ankle_UpDown] =       Motor(Right_Ankle_UpDown      ,Blocks[Right_Ankle   ],[ 2 , 3, 6 ,7 ],0               ,90         )
    Motors[Left_Ankle_Sideways] =      Motor(Left_Ankle_Sideways     ,Blocks[Left_Foot     ],[ 3 , 7, 2, 6 ],0.22            ,88         )
    Motors[Left_Ankle_UpDown] =        Motor(Left_Ankle_UpDown       ,Blocks[Left_Ankle    ],[ 6 , 7, 2 ,3 ],0               ,90         )
    
    # Motors[Right_Shoulder_UpDown                      ].rotate(45       +   30)
    # Motors[Right_Shoulder_Sideways                    ].rotate(83       +   30)
    # Motors[Right_Wrist                                ].rotate(20       +   30)
    # Motors[Left_Shoulder_Sideways                     ].rotate(130      +   30)
    # Motors[Left_Shoulder_UpDown                       ].rotate(0        +   30)
    # Motors[Left_Wrist                                 ].rotate(85       +   30)
    # Motors[Right_Pelvis_Sideways                      ].rotate(154      +   30)
    # Motors[Right_Pelvis_UpDown                        ].rotate(82       +   30)
    # Motors[Right_Knee                                 ].rotate(8        +   30)
    # Motors[Right_Ankle_UpDown                         ].rotate(80       +   30)
    # Motors[Right_Ankle_Sideways                       ].rotate(170      +   30)
    # Motors[Left_Pelvis_Sideways                       ].rotate(0        +   30)
    # Motors[Left_Pelvis_UpDown                         ].rotate(78       +   30)
    # Motors[Left_Knee                                  ].rotate(90       +   30)
    # Motors[Left_Ankle_UpDown                          ].rotate(88       +   30)
    # Motors[Left_Ankle_Sideways                        ].rotate(90       +   30)
    Angles=[45.0, 0.0, 83.0, 130.0, 0.0, 85.0, 154.0, 82.0, 170.0, 90.0, 78.0, 8.0, 80.0, 0.0, 90.0, 88.0]



    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Receiver waiting for connections...")
        conn, addr = server_socket.accept()
        print("Connected by", addr)
        with conn:
            conn.settimeout(0.02)
            while True:
                for event in pygame.event.get():
                    if event.type==pygame.KEYDOWN:
                        if (event.key==pygame.K_ESCAPE):
                            pygame.quit()
                            quit()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEMOTION:
                        mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
                        pygame.mouse.set_pos(displayCenter)
                        glRotatef(0.1*mouseMove[0],0,1,0)
                        view_angle+=0.1*mouseMove[0]
                key= pygame.key.get_pressed()
                if(not Hold_Shift or (Hold_Shift and ( key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT]))):
                    if(key[pygame.K_w]):
                        glTranslatef(-0.2*sin(view_angle),0,0.2*cos(view_angle))
                    elif(key[pygame.K_s]):
                        glTranslatef(0.2*sin(view_angle),0,-0.2*cos(view_angle))

                    if(key[pygame.K_q] or key[pygame.K_SPACE] or key[13] or key[10]):
                        glTranslatef(0,-0.2,0)
                    elif(key[pygame.K_e]or (not Hold_Shift and ( key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT]))):
                        glTranslatef(0,0.2,0)

                glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
                # Motors[Right_Shoulder_UpDown].rotate(rot_angle)#to be deleted
                # rot_angle=(rot_angle+0.5)%90
                # print(rot_angle)
                try:
                    packet = conn.recv(65536)  # Receive a fixed-size packet
                    if not packet:
                        break
                    
                    # Unpack the data from the received packet
                    if len(packet) >63:
                        Angles = unpack_data(packet[-64:])
                    else:
                        Angles = [45.0, 0.0, 83.0, 130.0, 0.0, 85.0, 154.0, 82.0, 170.0, 90.0, 78.0, 8.0, 80.0, 0.0, 90.0, 88.0111]
                except:
                    pass
                
                for i in range(16):
                    Motors[i].rotate(Angles[i])
                glBegin(GL_QUADS)
                glColor4fv((0.5,0.5,0.5,1))
                glVertex3fv([70,0,-70])
                glColor4fv((0.2,0.2,0.2,1))
                glVertex3fv([-70,0,-70])
                glColor4fv((0.5,0.5,0.5,1))
                glVertex3fv([-70,0,70])
                glColor4fv((0.2,0.2,0.2,1))
                glVertex3fv([70,0,70])
                glColor3fv((0,0,0))
                glEnd()

                if not disable_Sticky:
                    Stick_to_ground()

                for each in Blocks:
                    each.draw()

                # ******************************************
                # for i in range (len( Blocks)):
                #     if(i!=Head):
                #         each=Blocks[i]
                #         each.draw()
                # glBegin(GL_QUADS)
                # surface=Blocks[Head].surfaces[4]
                # glColor4fv((0.9,0.9,0.9,1))
                # for vertex in surface:
                #     glVertex3fv(Blocks[Head].corner[vertex])
                # surface=Blocks[Head].surfaces[5]
                # glColor4fv((0.9,0.9,0,1))
                # for vertex in surface:
                #     glVertex3fv(Blocks[Head].corner[vertex])
                # glColor3fv((0,0,0))
                # glEnd()
                #***********************************To be deleted(only for my ref while testing)

                pygame.display.flip()
                pygame.time.wait(30)
Blocks=[0]*18
Motors=[0]*16
main()