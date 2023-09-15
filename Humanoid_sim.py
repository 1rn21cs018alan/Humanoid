from OpenGL.GLUT import *  
from OpenGL.GL import *  
from OpenGL.GLU import *  
import pygame
from pygame.locals import *
import math

def sin(val):
    return math.sin(val*0.01745)
def cos(val):
    return math.cos(val*0.01745)

colors={'red':(1,0,0,1),
        'green':(0,1,0,1),
        'blue':(0,0,1,1),
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
            glColor4fv([(1,0,0,1),(0,1,0,1),(0,0,1,1),(1,1,1,1),(0.5,0.5,0.5,1),(0.75,0.75,0.75,1),][i])
            # if(i%2!=0):
            #     glColor4fv(self.color)
            for vertex in surface:
                self.corner[vertex]
                point=(self.corner[vertex][0]+coords[0], self.corner[vertex][1]+coords[1],self.corner[vertex][2]+coords[2])
                glVertex3fv(point)
        glColor3fv((0,0,0))
        glEnd()

        



def main():
    pygame.init()
    display = (800,600)
    displayCenter=(display[0]/2,display[1]/2)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    gluPerspective(65, (display[0]/display[1]), 0.1, 50.0)
    view_angle=0
    glTranslatef(0,0,-5)
    # prev=None
    # cam=[0,0,0]
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
                # view_angle=view_angle%360
        cam=glGetDoublev(GL_MODELVIEW_MATRIX)[3][:3]
        # cam=[cam[0],cam[1],cam[2]]
        # if(prev!=None):
        #     for i in range(3):
        #         if cam[i]!=prev[i]:
        #             print(cam)
        #             break
        # prev=cam
        key= pygame.key.get_pressed()
        if(key[pygame.K_RSHIFT] or key[pygame.K_LSHIFT] or True):
            if(key[pygame.K_w]):
                glTranslatef(-0.1*sin(view_angle),0,0.1*cos(view_angle))
            elif(key[pygame.K_s]):
                glTranslatef(0.1*sin(view_angle),0,-0.1*cos(view_angle))
            # elif(key[pygame.K_d]):
            #     glTranslatef(-0.1*cos(view_angle),0,-0.1*sin(view_angle))
            # elif(key[pygame.K_a]):
            #     glTranslatef(0.1*cos(view_angle),0,0.1*sin(view_angle))

            if(key[pygame.K_q]):
                glTranslatef(0,-0.1,0)
            elif(key[pygame.K_e]):
                glTranslatef(0,0.1,0)


        # glRotatef(1,0,1,0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        block1=CuboidBlock(2,2,2)
        block1.draw_surface()
        block2=CuboidBlock(1,1,1)
        # block2.draw_edge()
        block2.draw_edge((1,1,1))
        block1.draw_edge()


        pygame.display.flip()
        pygame.time.wait(30)


main()