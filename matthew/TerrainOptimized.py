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
        self.scaling_factor = 50  # Scale heights to scaling_factor units max
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
        self.buildQuadTree()

        self.buildRenderList()

    def buildQuadTree(self):
        self.polygons = self.find_quads(0, self.width-1, 0, self.height-1)
        print "%d polygons" % len(self.polygons)

        self.doh = glGenLists(2)
        glNewList(1, GL_COMPILE_AND_EXECUTE)

        glColor3f(0, 0, 1)
        #glMaterial(GL_FRONT, GL_AMBIENT, (0, .6, .2));
        glTranslatef(-self.width / 2, 0, -self.height/2)

        for start_x, end_x, start_y, end_y in self.polygons:
            glBegin(GL_QUADS)
            glVertex3f(start_x, self.heights[start_y][start_x], start_y)
            glVertex3f(start_x, self.heights[end_y][start_x], end_y)
            glVertex3f(end_x, self.heights[end_y][end_x], end_y)
            glVertex3f(end_x, self.heights[start_y][end_x], start_y)
            glEnd()
        glEndList()


    def coplanar(self, start_x, end_x, start_y, end_y):
        wiggle = 1

        #print start_x, start_y, end_x, end_y

        slope_x = (self.heights[end_x][start_y] - self.heights[start_x][start_y]) / float(end_x - start_x)
        slope_y = (self.heights[start_x][end_y] - self.heights[start_x][start_y]) / float(end_y - start_y)

        num_points = int(5 * ((end_x - start_x) * (end_y - start_y)))
        for i in range(num_points):
            px = random.randrange(start_x, end_x)
            py = random.randrange(start_y, end_y)
            actual_height = self.heights[py][px]
            estimated_height = (px - start_x) * slope_x + (py - start_y) * slope_y
            if abs(actual_height - estimated_height) > wiggle:
                return False

        return True


    def find_quads(self, start_x, end_x, start_y, end_y):
        min_resolution = 3
        interval = min(end_x - start_x, end_y - start_y)

        if interval < min_resolution or self.coplanar(start_x, end_x, start_y, end_y):
            return [(start_x, end_x, start_y, end_y)]

        else:
            new_interval = interval/2
            ul = self.find_quads(start_x, start_x+new_interval, start_y, start_y+new_interval)
            ur = self.find_quads(start_x+new_interval, end_x, start_y, start_y+new_interval)
            ll = self.find_quads(start_x, start_x+new_interval, start_y+new_interval, end_y)
            lr = self.find_quads(start_x+new_interval, end_x, start_y+new_interval, end_y)
            return ul + ur + ll + lr




    def optimizedRender(self):

        glCallList(1)



    def buildQuadTree2(self):
        self.polygons = self.find_quads(0, self.width-1, 0, self.height-1)
        print "%d polygons" % len(self.polygons)

    def all_same_height2(self, start_x, end_x, start_y, end_y):
        #print start_y, start_x
        height = self.heights[start_y][start_x]
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.heights[y][x] != height:
                    return False
        return True


    def find_quads2(self, start_x, end_x, start_y, end_y):
        min_resolution = 3
        interval = end_x - start_x
        if self.all_same_height(start_x, end_x, start_y, end_y) or interval < min_resolution:
            height = self.heights[start_y][start_x]
            return [(start_x, end_x, start_y, end_y, height)]
        else:
            new_interval = interval/2
            ul = self.find_quads(start_x, start_x+new_interval, start_y, start_y+new_interval)
            ur = self.find_quads(start_x+new_interval, end_x, start_y, start_y+new_interval)
            ll = self.find_quads(start_x, start_x+new_interval, start_y+new_interval, end_y)
            lr = self.find_quads(start_x+new_interval, end_x, start_y+new_interval, end_y)
            return ul + ur + ll + lr

    def optimizedRender2(self):
        glColor3f(0, 0, 1)
        glTranslatef(-self.width / 2, 0, -self.height/2)

        for start_x, end_x, start_y, end_y, height in self.polygons:
            glBegin(GL_QUADS)
            glVertex3f(start_x, height, start_y)
            glVertex3f(start_x, height, end_y)
            glVertex3f(end_x, height, end_y)
            glVertex3f(end_x, height, start_y)
            glEnd()


        

    def buildRenderList(self):

        glNewList(2, GL_COMPILE_AND_EXECUTE)
        glColor3f(0, 0, 1)
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
