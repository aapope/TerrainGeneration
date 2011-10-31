from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import random
import Image

from camera import *

class Terrain:

    def __init__(self):

        self.width = -1
        self.height = -1
        self.scaling_factor = 25  # Scale heights to scaling_factor units max
        self.heights = []

        self.polygons = []



    def load(self, filename):
        '''Load a heightmap bitmap file into the Terrain.
        Store the terrain as a list of rectangles (openGL quads).
'''      
        im = Image.open(filename)
        self.width = im.size[0]
        self.height = im.size[1]
        self.heights = []
        
        # Down the rows
        for y in range(self.height):
            row = []

            # Across the columns
            for x in range(self.width):
                pix = (im.getpixel((y, x)) / 255.) * self.scaling_factor
                row.append(pix)
            self.heights.append(row)

        self.buildRenderList()


    def buildRenderList(self):
        glNewList(2, GL_COMPILE)
        glMaterial(GL_FRONT, GL_DIFFUSE, (.1, .6, .34));
        glColor3f(0, .4, .1)

        glTranslatef(-self.width / 2, 0, -self.height/2)

        for x in range(0, self.width-1):
            glBegin(GL_QUAD_STRIP)

            glVertex3f(x, self.heights[0][x], 1)
            glVertex3f(x+1, self.heights[1][x], 1)
            for y in range(0, self.height-1):
                glVertex3f(x, self.heights[y][x], y)
                glVertex3f(x+1, self.heights[y][x+1], y)
            glEnd()
        glEndList()

    def render(self):
        glCallList(2)

if __name__ == '__main__': 
	terr = Terrain()
        terr.loadTerrain("../heightmaps/hill3.bmp")
