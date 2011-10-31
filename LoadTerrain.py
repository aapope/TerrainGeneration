import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class LoadTerrain:
    X_FACTOR = 1
    Y_FACTOR = 25
    Z_FACTOR = 1

    def __init__(self, filename):
        self.im = Image.open(filename)
        self.width = self.im.size[0]
        self.height = self.im.size[1]

    
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
                pix = (self.im.getpixel((y, x)) / 255.) * self.Y_FACTOR
                row.append(pix)
            heights.append(row)

        return heights

    def createRenderList(self, heights):
        glNewList(1, GL_COMPILE)

        for y in range(1, len(heights)):
            glBegin(GL_TRIANGLE_STRIP)
            for x in range(len(heights[y])):
                glVertex3f(x*self.X_FACTOR, heights[y][x], y*self.Z_FACTOR)
                glVertex3f(x*self.X_FACTOR, heights[y-1][x], y-1*self.Z_FACTOR)
            glEnd()
        glEndList()
