from PIL import Image, ImageDraw
from random import choice
import random, numpy, os

class RenderTexture:

    counter = 1
    SL = (-1,1,-1,1,-1,1)#Sun location: (left, right, bottom, top, near, far)

    def __init__(self, heights, scale):
 #       self.SIZE = scale[0]
        self.size = (len(heights)*scale[2], len(heights[0])*scale[0])
        self.texture = Image.new("RGB", (self.size[1], self.size[0]))
        self.scale = scale
        self.heights = heights

    def run(self, heights):
        self.load_bitmaps()
        self.create_texture(self.texture.load())
        path = 'data/textures/texture'+str(self.counter)+'.bmp'
        self.texture.save(path)
        self.counter += 1
        return path
        
    def load_bitmaps(self):
        self.images = {}
        img = self.get_rand_img('data/textures/tundra')
        self.images['tundra'] = (Image.open('data/textures/tundra/'+img).load(),Image.open('data/textures/tundra/'+img).size)
        img = self.get_rand_img('data/textures/deciduous')
        self.images['deciduous'] = (Image.open('data/textures/deciduous/'+img).load(),Image.open('data/textures/deciduous/'+img).size)
        img = self.get_rand_img('data/textures/savanna') 
        self.images['savanna'] = (Image.open('data/textures/savanna/'+img).load(),Image.open('data/textures/savanna/'+img).size)
        img = self.get_rand_img('data/textures/dirt') 
        self.images['dirt'] = (Image.open('data/textures/dirt/'+img).load(),Image.open('data/textures/dirt/'+img).size)
        img = self.get_rand_img('data/textures/treeline') 
        self.images['treeline'] = (Image.open('data/textures/treeline/'+img).load(),Image.open('data/textures/treeline/'+img).size)
        img = self.get_rand_img('data/textures/mountain') 
        self.images['mountain'] = (Image.open('data/textures/mountain/'+img).load(),Image.open('data/textures/mountain/'+img).size)
        img = self.get_rand_img('data/textures/grass') 
        self.images['grass'] = (Image.open('data/textures/grass/'+img).load(),Image.open('data/textures/grass/'+img).size)

    def create_texture(self, pix):
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                #get type of texture and its size
                pixl, sizel = self.images[self.texture_type(self.heights[x/self.scale[0]][y/self.scale[2]], 0)]
                #place according pixel of texture into terrain
                pix[y,x] = pixl[x%sizel[0], y%sizel[1]]

    def get_rand_img(self, path):
        tmp_imgs= []
        for subdir, dirs, imgs in os.walk(path):
            for img in imgs:
                tmp_imgs.append(img)
        return choice(tmp_imgs)

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
        else:
            return 'savanna'


