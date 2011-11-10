import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from RenderTexture import RenderTexture
from LinAlgOps import *
import os
from TextureHolder import TextureHolder

class LoadTerrain:

    def __init__(self, filename, convert, tex_holder):
        self.filename = filename
        self.convert = convert
        self.tex_holder = tex_holder
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
        

        rend = RenderTexture(heights, self.convert, self.tex_holder)#, face_norms)
        self.texture = self.tex_holder.hold_my_texture(rend.run(self.filename.split('/')[-1]), self.filename.split('/')[-1])

        water = 'data/textures/water/water2.bmp'
        water_tex = self.tex_holder.hold_my_texture(water, 'water')

        index = glGenLists(1)

        glNewList(index, GL_COMPILE)
        self.tex_holder.applyTexture(self.texture)

        for x in range(1, len(heights)):
            glBegin(GL_TRIANGLE_STRIP)
            for z in range(len(heights[x])):
                glTexCoord2f(self.convert.convert('h', 'g', 'x', x)/float(self.convert.gl_x), self.convert.convert('h', 'g', 'z', -z)/float(self.convert.gl_z))

                pt = (self.convert.convert('h', 'g', 'x', x), heights[x][z], self.convert.convert('h','g','z',-z))
                norm = vert_norms[pt]
                glNormal3f(norm[0],norm[1],norm[2])
                glVertex3f(pt[0],pt[1],pt[2])

                
                glTexCoord2f(self.convert.convert('h', 'g', 'x', x-1)/float(self.convert.gl_x), self.convert.convert('h', 'g', 'z', -z)/float(self.convert.gl_z))

                pt = (self.convert.convert('h', 'g', 'x', x-1), heights[x-1][z], self.convert.convert('h','g','z',-z))
                norm = vert_norms[pt]
                glNormal3f(norm[0],norm[1],norm[2])
                glVertex3f(pt[0],pt[1],pt[2])
            glEnd()
                

        '''Water plane'''
        self.tex_holder.applyTexture(water_tex)
        tile_size = Image.open(water).size
        xlen = self.convert.gl_x
        zlen = self.convert.gl_z
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(0, self.convert.sea_level, 0)
        glTexCoord2f(xlen/tile_size[0],0)
        glVertex3f(xlen, self.convert.sea_level, 0)
        glTexCoord2f(xlen/tile_size[0],zlen/tile_size[1])
        glVertex3f(xlen, self.convert.sea_level, -zlen)
        glTexCoord2f(0,zlen/tile_size[1])
        glVertex3f(0, self.convert.sea_level, -zlen)
        glEnd()

        glEndList()

        return index

    
