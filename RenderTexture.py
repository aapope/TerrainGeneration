from PIL import Image, ImageDraw
from random import choice
import random, numpy, os
import LinAlgOps
class RenderTexture:

    counter = 1
    SL = (-1,1,-1,1,-1,1)#Sun location: (left, right, bottom, top, near, far)
    SHADE = 40
    SUN_ANGLE = 0.3
    FACTOR = 10

    def __init__(self, heights, scale, norms):
        self.scale = (scale[0]*self.FACTOR, scale[1], scale[2]*self.FACTOR)
        self.SUN_ANGLE = scale[1]*.0008
        self.size = (len(heights)*self.scale[2], len(heights[0])*self.scale[0])
        self.texture = Image.new("RGB", (self.size[1], self.size[0]))
        self.heights = heights
        self.norms = norms

    def run(self, heights):
        self.load_bitmaps()
        self.create_texture(self.texture.load())
        #self.shadow(self.texture.load(), heights)
        return self.save()

    def save(self):
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
        img = self.get_rand_img('data/textures/deadgrass') 
        self.images['deadgrass'] = (Image.open('data/textures/deadgrass/'+img).load(),Image.open('data/textures/deadgrass/'+img).size)

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
            return 'deadgrass'
        elif temp < 20.5:
            return 'dirt'
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
    
    def shadow_diagonal(self, pixels, zs):
        for y in range(self.size[0]):
            col = y
            row = 0
            highest = self.calc_height(0, y, zs) - self.SUN_ANGLE
            while col < self.size[0] and row < self.size[1]:
                z = self.calc_height(row, col, zs)
                if z > highest:
                    highest = z
                else:
                    pixels[col, row] = self.darken(pixels[col, row], self.SHADE)
                highest -= self.SUN_ANGLE
                row += 1
                col += 1
                

            
    '''def calc_height(self, x, y, zs):
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
            return z'''

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
