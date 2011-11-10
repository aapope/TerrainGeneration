import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from RenderTexture import RenderTexture
from LinAlgOps import *

class LoadTerrain:
    X_FACTOR = 1
    Y_FACTOR = 1
    Z_FACTOR = 1
    SEA_LEVEL = 2
    counter = 1

    def __init__(self, filename, convert):
        self.convert = convert
        self.im = Image.open(filename)
        self.convert.set_dimensions(self.im.size[0], self.im.size[1])
        self.images = []
    
    def load(self):
        '''Load a heightmap bitmap file into the Terrain.
        Store the terrain as a list of rectangles (openGL quads).
        '''      
        heights = []
        
        # Down the rows
        for x in range(self.convert.heightmap_x):
            col = []

            # Across the columns
            for z in range(self.convert.heightmap_z):
                try:
                    pix = (self.im.getpixel((x, z)) / 255.) * self.convert.open_gl_scale[1]
                except:
                    pass
                col.append(pix)
            heights.append(col)
    
        return heights

    def createRenderList(self, heights):
        #face_norms is dict of face (3-tuple of vertices defining face, counterclockwise
        #starting from the upper left) : face normal
        #vert_norms is dict of vertex : normal
        face_norms, vert_norms = calc_face_normals(heights, self.convert)
        
        rend = RenderTexture(heights, self.convert, face_norms)
        self.texture = self.loadTexture(rend.run(heights), 0)
        
        water = 'data/textures/water/water2.bmp'
        water_tex = self.loadTexture(water, 1)

        index = glGenLists(1)

        glNewList(index, GL_COMPILE)
        self.applyTexture(self.texture)

        for x in range(1, len(heights)):
            glBegin(GL_TRIANGLE_STRIP)
            for z in range(len(heights[x])):
                glTexCoord2f(x*self.X_FACTOR/float(len(heights)*self.X_FACTOR),-z*self.Z_FACTOR/float(len(heights[x])*self.Z_FACTOR))
                pt = (x*self.convert.open_gl_scale[0], heights[x][z], -z*self.convert.open_gl_scale[2])
                norm = vert_norms[pt]
                glNormal3f(norm[0],norm[1],norm[2])
                glVertex3f(pt[0],pt[1],pt[2])

                glTexCoord2f(x*self.X_FACTOR/float(len(heights)*self.X_FACTOR),-(z-1)*self.Z_FACTOR/float(len(heights[x])*self.Z_FACTOR))
                pt = (x*self.convert.open_gl_scale[0], heights[x][z-1], -(z-1)*self.convert.open_gl_scale[2])
                norm = vert_norms[pt]
                glNormal3f(norm[0],norm[1],norm[2])
                glVertex3f(pt[0],pt[1],pt[2])
            glEnd()
                

        '''Water plane'''
        self.applyTexture(water_tex)
        tile_size = Image.open(water).size
        xlen = self.convert.gl_x
        zlen = self.convert.gl_z
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
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
