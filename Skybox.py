from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Image

class Skybox:
    #5 is the top; 3 has the sun
    FILES = ['data/textures/box/1sky1.bmp', 'data/textures/box/1sky2.bmp', 'data/textures/box/1sky3.bmp', 'data/textures/box/1sky4.bmp', 'data/textures/box/1sky5.bmp', 'data/textures/water/water.bmp']

    def __init__(self, (x, y, z)):
        self.x = x
        self.y = x/2.06
        self.z = -z
        self.texs = []

    def createCallList(self, call_index, tex_index):
        ids = self.loadTexture(tex_index)
        index = glGenLists(1)
        
        glNewList(index, GL_COMPILE)
        
        self.applyTexture(ids[0])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(0,0,0)
        glTexCoord2f(1, 1) ; glVertex3f(0,self.y,0)
        glTexCoord2f(0, 1) ; glVertex3f(self.x,self.y,0)
        glTexCoord2f(0, 0) ; glVertex3f(self.x,0,0)
        glEnd()

        self.applyTexture(ids[3])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(self.x,0,0)
        glTexCoord2f(1, 1) ; glVertex3f(self.x,self.y,0)
        glTexCoord2f(0, 1) ; glVertex3f(self.x,self.y,self.z)
        glTexCoord2f(0, 0) ; glVertex3f(self.x,0,self.z)
        glEnd()

        self.applyTexture(ids[2])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(self.x,0,self.z)
        glTexCoord2f(1, 1) ; glVertex3f(self.x,self.y,self.z)
        glTexCoord2f(0, 1) ; glVertex3f(0,self.y,self.z)
        glTexCoord2f(0, 0) ; glVertex3f(0,0,self.z)
        glEnd()

        self.applyTexture(ids[1])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(0,0,self.z)
        glTexCoord2f(1, 1) ; glVertex3f(0,self.y,self.z)
        glTexCoord2f(0, 1) ; glVertex3f(0,self.y,0)
        glTexCoord2f(0, 0) ; glVertex3f(0,0,0)
        glEnd()
        
        self.applyTexture(ids[4])
        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex3f(0,self.y,0)
        glTexCoord2f(1, 1) ; glVertex3f(self.x,self.y,0)
        glTexCoord2f(0, 1) ; glVertex3f(self.x,self.y,self.z)
        glTexCoord2f(0, 0) ; glVertex3f(0,self.y,self.z)
        glEnd()

        glEndList()

        return index

    def loadTexture(self, i):
        texId = []
        for t in range(len(self.FILES)):
            texId.append(i)
            glGenTextures(1, texId[t])
            glBindTexture(GL_TEXTURE_2D, texId[t])
            self.texs.append(Image.open(self.FILES[t]))
            glTexImage2D(GL_TEXTURE_2D, 0, 3, self.texs[-1].size[0], self.texs[-1].size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.texs[-1].tostring("raw","RGBX",0,-1))
            i += 1
        return texId

    def applyTexture(self, tex_id):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        #glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        '''glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)'''
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
