from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import os, Image
from random import choice

class TextureHolder:
    index_counter = 1

    def __init__(self):
        self.images = {}
        self.texture_ids = {}
        self.load_bitmaps()

    def load_bitmaps(self):
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

    def hold_my_texture(self, filename, name):
        self.texture_ids[name] = self.index_counter
        glGenTextures(1, self.texture_ids[name])
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[name])
        self.images[name] = Image.open(filename)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.images[name].size[0], self.images[name].size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.images[name].tostring("raw","RGBX",0,-1))
        self.index_counter += 1
        return name

    def applyTexture(self, name):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_ids[name])
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    def get_rand_img(self, path):
        tmp_imgs= []
        for subdir, dirs, imgs in os.walk(path):
            for img in imgs:
                tmp_imgs.append(img)
        return choice(tmp_imgs)
