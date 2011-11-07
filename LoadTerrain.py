import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from RenderTexture import RenderTexture
from LinAlgOps import *

class LoadTerrain:
    X_FACTOR = 10
    Y_FACTOR = 350
    Z_FACTOR = 10
    MAP_SIZE = 100
    SEA_LEVEL = Y_FACTOR/20
    counter = 1

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
        rend = RenderTexture(heights, (self.X_FACTOR, self.Y_FACTOR, self.Z_FACTOR))
        self.texture = self.loadTexture(rend.run(heights), 0)
        water = 'data/textures/water.bmp'
        water_tex = self.loadTexture(water, 1)
        #Calculate the normals for each face, stored in a dict of 
        #point : norms offaces with that point
        face_norms = calc_face_normals(heights, self.X_FACTOR, self.Z_FACTOR)
        index = glGenLists(1)
        glNewList(index, GL_COMPILE)

        self.applyTexture(self.texture)

        for y in range(1, len(heights)):
            glBegin(GL_TRIANGLE_STRIP)
            for x in range(len(heights[y])):
                #glTexCoord2f(x*self.X_FACTOR/float(len(heights[y])*self.X_FACTOR),-y*self.Z_FACTOR/float(len(heights)*self.Z_FACTOR))
                glTexCoord2f(-(len(heights)-y)*self.Z_FACTOR/float(len(heights)),-x*self.X_FACTOR/float(len(heights[y])))
                pt = (x*self.X_FACTOR, heights[y][x], -y*self.Z_FACTOR)
                #calculate the point's normal
                norm = calc_vert_normals(pt,face_norms)
                glNormal3f(norm[0],norm[1],norm[2])
                glVertex3f(pt[0],pt[1],pt[2])

                glTexCoord2f(-(len(heights)-y+1)*self.Z_FACTOR/float(len(heights)),-x*self.X_FACTOR/float(len(heights[y-1])))
                pt = (x*self.X_FACTOR, heights[y-1][x], -(y-1)*self.Z_FACTOR)
                norm = calc_vert_normals(pt, face_norms)
                glNormal3f(norm[0],norm[1],norm[2])
                glVertex3f(pt[0],pt[1],pt[2])

                '''self.newTexture(heights[y][x],0)
                glBegin(GL_TRIANGLE_STRIP)
                glTexCoord2f(0,0)
>>>>>>> 01864d7bd1ab817d291a0ebab20acbe988e7d36f
                glVertex3f(x*self.X_FACTOR, heights[y][x], -y*self.Z_FACTOR)
                glTexCoord2f(x*self.X_FACTOR/float(len(heights[y])*self.X_FACTOR),-(y-1)*self.Z_FACTOR/float(len(heights)*self.Z_FACTOR))
                glVertex3f(x*self.X_FACTOR, heights[y-1][x], -(y-1)*self.Z_FACTOR)'''
            glEnd()
                

        '''Water plane'''
        self.applyTexture(water_tex)
        tile_size = Image.open(water).size
        xlen = len(heights[0])*self.X_FACTOR
        zlen = len(heights)*self.Z_FACTOR
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(0, self.SEA_LEVEL, 0)
        glTexCoord2f(xlen/tile_size[0],0)
        glVertex3f(xlen, self.SEA_LEVEL, 0)
        glTexCoord2f(xlen/tile_size[0],zlen/tile_size[1])
        glVertex3f(xlen, self.SEA_LEVEL, -zlen)
        glTexCoord2f(0,zlen/tile_size[1])
        glVertex3f(0, self.SEA_LEVEL, -zlen)
        glEnd()

        glEndList()
        return index


    def loadTexture(self, filenames, i):
        texId = i
        glGenTextures(1, texId)
        glBindTexture(GL_TEXTURE_2D, texId)
        self.images.append(Image.open(filenames))
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
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


    def newTexture(self, altitude, percip):
        d_temp = altitude / 6.5
        temp = 20 - d_temp
        if temp <= 18:
            self.applyTexture(self.tex_list[0])
        elif temp < 20:
            self.applyTexture(self.tex_list[1])
        else:
            self.applyTexture(self.tex_list[2])
