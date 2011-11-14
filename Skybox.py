from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Image

class Skybox:
    #5 is the top; 3 has the sun
    FILES = ['data/textures/box/1sky1.bmp', 'data/textures/box/1sky2.bmp', 'data/textures/box/1sky3.bmp', 'data/textures/box/1sky4.bmp', 'data/textures/box/1sky5.bmp', 'data/textures/water/water.bmp']

    def __init__(self, tex_holder, (x, y, z)):
        self.x = x
        self.y = x/2.06
        self.z = -z
        self.tex_holder = tex_holder
        self.texs = []
        for i in range(len(self.FILES)):
            self.FILES[i] = tex_holder.hold_my_texture(self.FILES[i], 'skybox'+str(i))
            

    def createCallList(self, call_index, tex_index):
        
        index = glGenLists(1)
        
        glNewList(index, GL_COMPILE)
        
        self.tex_holder.applyTexture(self.FILES[0])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(0,0,0)
        glTexCoord2f(1, 1) ; glVertex3f(0,self.y,0)
        glTexCoord2f(0, 1) ; glVertex3f(self.x,self.y,0)
        glTexCoord2f(0, 0) ; glVertex3f(self.x,0,0)
        glEnd()

        self.tex_holder.applyTexture(self.FILES[3])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(self.x,0,0)
        glTexCoord2f(1, 1) ; glVertex3f(self.x,self.y,0)
        glTexCoord2f(0, 1) ; glVertex3f(self.x,self.y,self.z)
        glTexCoord2f(0, 0) ; glVertex3f(self.x,0,self.z)
        glEnd()

        self.tex_holder.applyTexture(self.FILES[2])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(self.x,0,self.z)
        glTexCoord2f(1, 1) ; glVertex3f(self.x,self.y,self.z)
        glTexCoord2f(0, 1) ; glVertex3f(0,self.y,self.z)
        glTexCoord2f(0, 0) ; glVertex3f(0,0,self.z)
        glEnd()

        self.tex_holder.applyTexture(self.FILES[1])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(0,0,self.z)
        glTexCoord2f(1, 1) ; glVertex3f(0,self.y,self.z)
        glTexCoord2f(0, 1) ; glVertex3f(0,self.y,0)
        glTexCoord2f(0, 0) ; glVertex3f(0,0,0)
        glEnd()
        
        self.tex_holder.applyTexture(self.FILES[4])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(0,self.y,0)
        glTexCoord2f(1, 1) ; glVertex3f(self.x,self.y,0)
        glTexCoord2f(0, 1) ; glVertex3f(self.x,self.y,self.z)
        glTexCoord2f(0, 0) ; glVertex3f(0,self.y,self.z)
        glEnd()

        glEndList()

        return index
