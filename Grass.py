from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Image

class Grass:
    
    #create a number of grass objects either for a map (in 
    #which case, send it the areas it can go in) or just
    #in general. Probably tie the render
    def __init__(self):
        pass
    
    def create_grass_list(self):
        item = glGenLists(1)
        ids = self.load_texture('l-system.png')
        glNewList(item, GL_COMPILE)
        self.applyTexture(ids)
        #glColor4f(0,0,0,0)

        glBegin(GL_QUADS)
        glTexCoord2f(1, 0) ; glVertex(0,0,0)
        glTexCoord2f(1, 1) ; glVertex(0,10,0)
        glTexCoord2f(0, 1) ; glVertex(10,10,0)
        glTexCoord2f(0, 0) ; glVertex(10,0,0)
        glEnd()

        glEndList()
        return item

    def load_texture(self, filename):
        glGenTextures(1, 1)
        glBindTexture(GL_TEXTURE_2D, 1)
        self.image = Image.open(filename)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.image.size[0], self.image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image.tostring("raw","RGBA",0,-1))
        return 1

    def applyTexture(self, name):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, name)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
