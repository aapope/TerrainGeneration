from PIL import Image, ImageDraw
from random import choice

class RenderTexture:
    counter = 1
    SIZE = 10

    def __init__(self, heights):
        self.size = (len(heights), len(heights[0]))
        self.texture = Image.new("RGB", (self.size[1]*self.SIZE, self.size[0]*self.SIZE))

    def run(self, heights):
        images = self.load_bitmaps()
        self.create_textures(images, heights, self.size)
        path = 'data/textures/texture'+str(self.counter)+'.bmp'
        self.texture.save(path)
        self.counter += 1
        return path
        
    def load_bitmaps(self):
        images = {}
        images['tundra'] = []
        images['tundra'].append(Image.open('data/textures/tundra.bmp'))

        images['deciduous'] = []
        images['deciduous'].append(Image.open('data/textures/deciduous.bmp'))

        images['savanna'] = []
        images['savanna'].append(Image.open('data/textures/savanna.bmp'))

        for key, value in images.items():
            for im in value:
                im.resize((self.SIZE,self.SIZE))        
        return images
        
    def create_textures(self, images, heights, size):
        for y in range(size[0]):
            for x in range(size[1]):
                h = heights[y][x]
                tex = self.texture_type(h, 0)
                im = choice(images[tex])
                self.texture.paste(im, (y*self.SIZE,x*self.SIZE))

    def texture_type(self, altitude, percip):
        d_temp = altitude / 6.5
        temp = 20 - d_temp
        if temp <= 18:
            return 'tundra'
        elif temp < 20:
            return 'deciduous'
        else:
            return 'savanna'
