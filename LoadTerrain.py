import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class LoadTerrain:
    X_FACTOR = 1
    Y_FACTOR = 25
    Z_FACTOR = 1
    MAP_SIZE = 100

    def __init__(self, filename):
        self.im = Image.open(filename)
        self.width = self.im.size[0]
        self.height = self.im.size[1]
        self.images = []
    
    def load(self):
        '''Load a heightmap bitmap file into the Terrain.
        Store the terrain as a list of rectangles (openGL quads).
'''      
        heights = []
        
        # Down the rows
        for y in range(self.height):
            row = []

            # Across the columns
            for x in range(self.width):
                try:
                    pix = (self.im.getpixel((y, x)) / 255.) * self.Y_FACTOR
                except:
                    pass
                row.append(pix)
            heights.append(row)

        return heights

    def createRenderList(self, heights):
        glNewList(1, GL_COMPILE)
        texture = self.loadTexture('checkerboard.bmp')
        self.applyTexture(texture)
        for y in range(1, len(heights)):
            glBegin(GL_TRIANGLE_STRIP)
            for x in range(len(heights[y])):
                glTexCoord2f(x*self.X_FACTOR/float(len(heights[y])), y*self.Z_FACTOR/float(len(heights)))
                glVertex3f(x*self.X_FACTOR, heights[y][x], y*self.Z_FACTOR)
                glTexCoord2f(x*self.X_FACTOR/float(len(heights[y-1])), y*self.Z_FACTOR/float(len(heights)))
                glVertex3f(x*self.X_FACTOR, heights[y-1][x], y-1*self.Z_FACTOR)
            glEnd()
        glEndList()

    def loadTexture(self, filename):
        texId = 0
        glGenTextures(1, texId)
        glBindTexture(GL_TEXTURE_2D, texId)
        self.images.append(Image.open(filename))
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.images[-1].size[0], self.images[-1].size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.images[-1].tostring("raw","RGBX",0,-1))
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
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
