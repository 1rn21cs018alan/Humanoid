from OpenGL.GLUT import *  
from OpenGL.GL import *  
from OpenGL.GLU import *  
import pygame
from pygame.locals import *
import math
from __constants import *
def sin(val):
    return math.sin(val*0.01745)
def cos(val):
    return math.cos(val*0.01745)

colors={'red':(1,0,0,1),
        'green':(0,1,0,1),
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
                    self.corner.append((i*h,j*w,d*k))
        
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
            (1,3,7,5),
            (2,3,7,6),
            (2,0,4,6),
        )
        self.pos={'x':0,'y':0}
    
    def draw_edge(self,coords=(0,0,0)):
        glBegin(GL_LINES)
        glColor4fv(colors['red'])
        for edge in self.edges:
            for vertex in edge:
                self.corner[vertex]
                point=(self.corner[vertex][0]+coords[0], self.corner[vertex][1]+coords[1],self.corner[vertex][2]+coords[2])
                glVertex3fv(point)
        glColor3fv((0,0,0))
        glEnd()
    
    def draw_surface(self,coords=(0,0,0)):
        glBegin(GL_QUADS)
        for i in range(len(self.surfaces)):
            surface=self.surfaces[i]
            glColor4fv(self.color)
            for vertex in surface:
                self.corner[vertex]
                point=(self.corner[vertex][0]+coords[0], self.corner[vertex][1]+coords[1],self.corner[vertex][2]+coords[2])
                glVertex3fv(point)
        glColor3fv((0,0,0))
        glEnd()


class FreeBlock(CuboidBlock):
    def __init__(self, Height, Width, Depth, color=colors['light grey'],loc=[0,0,0]):
        super().__init__(Height, Width, Depth, color)
        self.loc=loc
        self.angle_V=angle

    def draw(self):
        self.draw_surface(self.loc)
        self.draw_edge(self.loc)
    
    def set_coords(coords):
        self.loc=coords
    
    def update_vector(angle):
        self.angle_v





def main():
    pygame.init()
    display = (1200,800)
    displayCenter=(display[0]/2,display[1]/2)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    gluPerspective(65, (display[0]/display[1]), 0.1, 70.0)
    view_angle=0
    glTranslatef(0,-10,-25)
    Blocks=[0]*18
    Blocks[Head]=FreeBlock(1,1,1,loc=[0,15.5,0],color=colors['blue'])
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
        if(key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT] or True):
            if(key[pygame.K_w]):
                glTranslatef(-0.2*sin(view_angle),0,0.2*cos(view_angle))
            elif(key[pygame.K_s]):
                glTranslatef(0.2*sin(view_angle),0,-0.2*cos(view_angle))

            if(key[pygame.K_q]):
                glTranslatef(0,-0.2,0)
            elif(key[pygame.K_e]):
                glTranslatef(0,0.2,0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for each in Blocks:
            each.draw()

        pygame.display.flip()
        pygame.time.wait(30)


main()