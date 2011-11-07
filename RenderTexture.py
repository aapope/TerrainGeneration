from PIL import Image, ImageDraw
from random import choice
import random

class RenderTexture:

    counter = 1

    def __init__(self, heights, scale):
        self.size = (len(heights)*scale[2], len(heights[0])*scale[0])
        self.texture = Image.new("RGB", (self.size[1], self.size[0]))
        self.scale = scale

    def run(self, heights):
        #images = self.load_bitmaps()
        self.load_bitmaps()
        self.create_texture(self.texture.load(), heights)
        path = 'data/textures/texture'+str(self.counter)+'.bmp'
        self.texture.save(path)
        self.counter += 1
        return path
        
    def load_bitmaps(self):
        self.images = {}
        self.images['tundra'] = (Image.open('data/textures/tundra1.bmp').load(),Image.open('data/textures/tundra1.bmp').size)

        self.images['deciduous'] = (Image.open('data/textures/grass.jpg').load(),Image.open('data/textures/grass.jpg').size)

        self.images['savanna'] = (Image.open('data/textures/sand.jpg').load(),Image.open('data/textures/sand.jpg').size)

    def create_texture(self, pix, heights):
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                #print 'Mapping ' +  str(self.texture_type(heights[x/self.scale[0]][y/self.scale[2]], 0)) +" "+ str(x/self.scale[0])+","+str(y/self.scale[2])+' to '+ str(x)+","+str(y)
                pixl, sizel = self.images[self.texture_type(heights[x/self.scale[0]][y/self.scale[2]], 0)]
                #pix[y,x] = self.randomize_color(pixl[x%sizel[0], y%sizel[1]], 25)
                pix[y,x] = pixl[x%sizel[0], y%sizel[1]]

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
        elevation = max_elevation*(altitude/float(self.scale[1]))
        d_temp = (elevation/1000) / 6.5 + random.uniform(-temp_blend,temp_blend)
        temp = 20 - d_temp
        if temp <= 19.5:
            return 'tundra'
        elif temp < 19.9:
            return 'deciduous'
        else:
            return 'savanna'
