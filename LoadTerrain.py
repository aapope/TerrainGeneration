import Image
from RenderTexture import RenderTexture
from LinAlgOps import *
import os
from TextureHolder import TextureHolder
import LinAlgOps

class LoadTerrain:
    X_FACTOR = 1
    Y_FACTOR = 1
    Z_FACTOR = 1
    MAP_SIZE = 100
    SEA_LEVEL = 4
    counter = 1


    def __init__(self, filename, convert, tex_holder):
        self.filename = filename
        self.convert = convert
        self.tex_holder = tex_holder
        self.im = Image.open(filename)
        self.convert.set_dimensions(self.im.size[0], self.im.size[1])
        self.images = []
	self.center = 0
	self.index  = 0  	

    def load(self):
        '''Load a heightmap bitmap file into the Terrain.
        Store the terrain as a list of triangle strips.
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

#<<<<<<< HEAD
    #def createRenderList(self, heights):
        #face_norms is dict of face (3-tuple of vertices defining face, counterclockwise
        #starting from the upper left) : face normal
        #vert_norms is dict of vertex : normal
        #face_norms, vert_norms = calc_face_normals(heights, self.convert)
        

        #rend = RenderTexture(heights, self.convert, self.tex_holder)#, face_norms)
        

        
#=======

    def createRenderList(self, heights, textname):
        #rend = RenderTexture(heights, (self.X_FACTOR, self.Y_FACTOR, self.Z_FACTOR))
	rend = RenderTexture(heights, self.convert, self.tex_holder)
	tex_file_name = rend.run(self.filename.split('/')[-1])
	face_norms, vert_norms = LinAlgOps.calc_face_normals(heights, self.convert)
	
	return (tex_file_name, face_norms, vert_norms)


