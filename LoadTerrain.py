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


    def createRenderList(self, heights, textname):
        #rend = RenderTexture(heights, (self.X_FACTOR, self.Y_FACTOR, self.Z_FACTOR))
        rend = RenderTexture(heights, self.convert, self.tex_holder)
        tex_file_name = rend.run(self.filename.split('/')[-1])
        print "start norms"
        face_norms, vert_norms = LinAlgOps.calc_face_normals(heights, self.convert)
        print "end norms"
        #return (tex_file_name, 0, 0)
        return (tex_file_name, face_norms, vert_norms)
