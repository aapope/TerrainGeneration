from PIL import Image, ImageDraw
from random import choice
import random, numpy, os
import LinAlgOps
from TextureHolder import TextureHolder

class RenderTexture:
#    SHADE = 40
#    SUN_ANGLE = 0.3

    def __init__(self, heights, convert, tex_holder):#norms):
        self.tex_holder = tex_holder
        self.convert = convert
        self.SUN_ANGLE = self. convert.open_gl_scale[1]*.0008
        self.texture = Image.new("RGB", (self.convert.texture_x, self.convert.texture_z))
        self.heights = heights
        #self.norms = norms        

    def initial_run(self, name):
        path = 'data/textures/maps/'+name
        #if not os.path.isfile(path):
        #print 'New texture'
        self.create_texture(self.texture.load())
        return self.save(path)
        #else:
            #return path
    
    def run(self, name):
	path = 'data/textures/maps/'+name
        if not os.path.isfile(path):
        	#print 'New texture'
        	self.create_texture(self.texture.load())
                #self.shadow(self.texture.load(), self.heights)
        	return self.save(path)
        else:
            return path	

    def save(self, path):
        self.texture.save(path)
        return path
    '''
    def run(self, heights, name):
	path = 'data/textures/texture'+name+'.bmp'	
	self.load_bitmaps()
	self.create_texture(self.texture.load())
	self.shadow(self.texture.load(), heights)
		
	self.texture.save(path)
	print path
	return path'''

    '''old RUN
    def run(self, heights):
        self.load_bitmaps()
        self.create_texture(self.texture.load())
        self.shadow(self.texture.load(), heights)
        path = 'data/textures/texture'+str(self.counter)+'.bmp'
        self.texture.save(path)
        self.counter += 1
        return path'''

        
    def create_texture(self, pix):
        for x in range(self.convert.texture_z):
            for z in range(self.convert.texture_x):
                #get type of texture and its size
                pixl,sizel = self.tex_holder.images[self.texture_type(self.heights[x/self.convert.texture_scale[0]][z/self.convert.texture_scale[2]], 0)]
                #pixl = img.load()
                #place according pixel of texture into terrain
                pix[x,z] = pixl[x%sizel[0], z%sizel[1]]


    def randomize_color(self, color, randomness=10):
        r,g,b = color
        r += random.randint(-randomness, randomness)
        g += random.randint(-randomness, randomness)
        b += random.randint(-randomness, randomness)

        r = min(max(r, 0), 255)
        g = min(max(g, 0), 255)
        b = min(max(b, 0), 255)

        return (r,g,b)
            
    def texture_type(self, altitude, percip):
        temp_blend = .04
        max_elevation = 5000
        elevation = max_elevation*(altitude/float(self.convert.gl_y))
        d_temp = (elevation/1000) / 6.5 + random.uniform(-temp_blend,temp_blend)
        temp = 20 - d_temp
        if temp <= 19.5:
            return 'tundra'
        elif temp < 19.65:
            return 'mountain'
        elif temp < 19.75:
            return 'treeline'
        elif temp < 19.85:
            return 'grass'
        elif temp < 19.9:
            return 'deciduous'
        elif temp < 20:
            return 'dirt'
        elif temp < 20.1:
            return 'deadgrass'
        else:
            return 'savanna'

    def shadow(self, pixels, zs):
        for y in range(1, self.size[0]):
            highest = self.calc_height(self.size[1]-2, y, zs) - self.SUN_ANGLE
            darkened = 4
            for x in range(self.size[1]-1, 1, -1):
                z = self.calc_height(x, y, zs)
#                print x/self.scale[0], y/self.scale[2], z
                if z > highest:
                    if darkened == 4:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE/30)
                    elif darkened == 3:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE/30)
                    if darkened == 2:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE/30)
                    elif darkened == 1:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE/20)
                    highest = z
                    darkened = max(0, darkened-1)
                else:
                    if darkened == 0:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE/20)
                    elif darkened == 1:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE/15)
                    elif darkened == 2:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE/10)
                    elif darkened == 3:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE/5)
                    else:
                        pixels[y, x] = self.darken(pixels[y, x], self.SHADE)
                    darkened += 1
                highest -= self.SUN_ANGLE
    
    def calc_height(self, x, y, zs):
        #pos_scale = (self.scale[0]
        #print zs
        x_gl = x/self.FACTOR
        y_gl = y/self.FACTOR
        x_hmap = x/self.scale[0]
        y_hmap = y/self.scale[2]


        p1 = (x_gl, zs[y_hmap][x_hmap], -y_gl)
        p2 = (x_gl-1, zs[y_hmap][x_hmap-1], -y_gl)
        p3 = (x_gl, zs[y_hmap+1][x_hmap], -y_gl-1)
        p4 = (x_gl-1, zs[y_hmap+1][x_hmap-1], -y_gl-1)

        scale_y = float(y)/self.FACTOR - y_gl
        scale_x = float(x)/self.FACTOR - x_gl

        if x % self.scale[0] == 0:
            if y % self.scale[2] == 0:
                return p1[1]
            else:                
                return (p1[1]*(1-scale_y)+p2[1]*scale_y)

        elif y % self.scale[2] == 0:
            return (p1[1]*(1-scale_x)+p3[1]*scale_x)

        else:
            if scale_x + scale_y == 1:
                norm = self.norms[(p2,p1,p3)]

            if scale_x + scale_y < 1:
                norm = self.norms[(p2,p1,p3)]

            elif scale_x + scale_y > 1:
                norm = self.norms[(p2,p3,p4)]

            
            z = -(norm[0]*(x-p3[0])+norm[1]*(y-p3[1]))/norm[2] + p3[2]
            print z
            return z

    def darken(self, pixel, amt):
        r,g,b = pixel
        r = max(0, r - amt)
        g = max(0, g - amt)
        b = max(0, b - amt)
        return (r,g,b)
