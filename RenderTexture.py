from PIL import Image, ImageDraw
from random import choice
import random

class RenderTexture:
    counter = 1
    SIZE = 10

    def __init__(self, heights):
        self.size = (len(heights)*self.SIZE, len(heights[0])*self.SIZE)
        self.texture = Image.new("RGB", (self.size[1], self.size[0]))

    def run(self, heights):
        #images = self.load_bitmaps()
        self.load_bitmaps()
        self.create_texture(self.texture.load(), heights, self.size)
        path = 'data/textures/texture'+str(self.counter)+'.bmp'
        self.texture.save(path)
        self.counter += 1
        return path
        
    def load_bitmaps(self):
        self.images = {}
        self.images['tundra'] = (Image.open('data/textures/tundra1.bmp').load(),Image.open('data/textures/tundra1.bmp').size)

        self.images['deciduous'] = (Image.open('data/textures/near_treeline.jpg').load(),Image.open('data/textures/near_treeline.jpg').size)

        self.images['savanna'] = (Image.open('data/textures/savanna1.bmp').load(),Image.open('data/textures/savanna1.bmp').size)

    def create_texture(self, pix, heights, size):
        for y in range(size[0]):
            for x in range(size[1]):
                pixl, sizel = self.images[self.texture_type(heights[y/self.SIZE][x/self.SIZE], 0)]
                pix[y,x] = self.randomize_color(pixl[x%sizel[0], y%sizel[1]], 25)

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
        d_temp = altitude / 6.5
        temp = 20 - d_temp
        if temp <= 18:
            return 'tundra'
        elif temp < 20:
            return 'deciduous'
        else:
            return 'savanna'
