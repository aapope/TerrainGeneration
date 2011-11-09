from PIL import Image, ImageDraw
from random import choice
import random, numpy, os

class RenderTexture:

    counter = 1
    SIZE = 20
    SL = (-1,1,-1,1,-1,1)#Sun location: (left, right, bottom, top, near, far)
    SHADE = 80

    def __init__(self, heights, scale):
 #       self.SIZE = scale[0]
        self.size = (len(heights)*scale[2], len(heights[0])*scale[0])
        self.texture = Image.new("RGB", (self.size[1], self.size[0]))
        self.scale = scale

    def run(self, heights):
        #images = self.load_bitmaps()
        self.load_bitmaps()
        self.create_texture(self.texture.load(), heights)
        #self.shadow(self.texture.load(), heights)
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
        img = self.get_rand_img('data/textures/treeline') 
        self.images['treeline'] = (Image.open('data/textures/treeline/'+img).load(),Image.open('data/textures/treeline/'+img).size)

    def create_texture(self, pix, heights):
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                #print 'Mapping ' +  str(self.texture_type(heights[x/self.scale[0]][y/self.scale[2]], 0)) +" "+ str(x/self.scale[0])+","+str(y/self.scale[2])+' to '+ str(x)+","+str(y)
                pixl, sizel = self.images[self.texture_type(heights[x/self.scale[0]][y/self.scale[2]], 0)]
                #pix[y,x] = self.randomize_color(pixl[x%sizel[0], y%sizel[1]], 25)
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
            return 'treeline'
        elif temp < 19.9:
            return 'deciduous'
        elif temp < 20:
            return 'dirt'
        else:
            return 'savanna'


    def shadow(self, pixels, zs):
        for y in range(self.size[0]):
            highest = self.calc_height(self.size[1]-1, y, zs) - 0.5
            darkened = False
            for x in range(self.size[1]-2,-1,-1):
                z = self.calc_height(x, y, zs)
                if z > highest:
                    if darkened:
                        pixels[y, x] = (100,0,100)#self.darken(pixels[y, x], self.SHADE/2)
                    highest = z
                    darkened = False
                else:
                    if not darkened:
                        pixels[y, max(x+1,0)] = self.darken(pixels[y, max(x+1,0)], self.SHADE/2)
                    pixels[y, x] = self.darken(pixels[y, x], self.SHADE)
                    darkened = True
                highest -= 0.5
                
    def calc_height(self, x, y, zs):
        p1 = zs[x/self.scale[0]][y/self.scale[2]]
        p2 = zs[x/self.scale[0]][min(y/self.scale[2]+1, len(zs[1])-1)]
        p3 = zs[min(x/self.scale[0]+1, len(zs)-1)][y/self.scale[2]]
        p4 = zs[min(x/self.scale[0]+1, len(zs)-1)][min(y/self.scale[2]+1, len(zs[1])-1)]

        scale_y = float(y)/self.scale[2] - y/self.scale[2]
        scale_x = float(x)/self.scale[0] - x/self.scale[0]

        if x % self.scale[0] == 0:
            if y% self.scale[2] == 0:
                return p1
            else:                
                return (p1*(1-scale_y)+p2*scale_y)

        elif y % self.scale[2] == 0:
            return (p1*(1-scale_x)+p3*scale_x)

        else:
            a1 = (p1*(1-scale_y) + p2*(scale_y))
            a2 = (p3*(1-scale_y) + p4*(scale_y))

            return (a1*(1-scale_x) + a2*scale_x)


    def darken(self, pixel, amt):
        r,g,b = pixel
        r = max(0, r - amt)
        g = max(0, g - amt)
        b = max(0, b - amt)
        return (r,g,b)
