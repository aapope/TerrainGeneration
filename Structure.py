from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random, math
from TextureHolder import TextureHolder

class Structure:
    
    WALL_SIZE = (10, 20)
    WALL_HEIGHT = 5
    GLASS_HEIGHT = (2, 3)
    WINDOW_SIZE = (3, 2)
    ROOMS = (1,3)
    OVERLAP = (4,3)
    BRICK_SIZE = (1, 1, 1) 
    HEIGHT = 4

    def __init__(self, tex_holder, structure_type=None):
        self.structure_type = structure_type
        self.direction = ['down', 'right', 'left', 'up']
        self.direction_inverse = ['up', 'left', 'right', 'down']
        self.textures = tex_holder

    def create_structure(self):
        x = self.WALL_SIZE[1]*5
        z = self.WALL_SIZE[1]*5
        blueprint = self.make_blueprint(x,z)
        blueprint = self.trim_blueprint(blueprint)
        blueprint = self.trace_blueprint(blueprint)
        blueprint = self.make_windows(blueprint)

        #for line in blueprint:
            #print line

        glColor4f(1,1,1,1)
        callback = self.create_callist(blueprint)

        return callback
        
    def create_callist(self, blueprint):
        callback = glGenLists(1)

        brick_img = self.textures.get_rand_img('data/textures/brick')
        print brick_img
        self.brick = self.textures.hold_my_texture('data/textures/brick/'+brick_img, brick_img)
        self.glass = self.textures.hold_my_texture('data/textures/random/glass.png', 'glass')

        glNewList(callback, GL_COMPILE)

        x = 0
        z = 0

        for fill_x in range(len(blueprint)):
            for fill_z in range(len(blueprint[x])):
                if blueprint[x][z] == 1: 
                    x = fill_x+1
                    z = fill_z+1
                    break

        height = self.WALL_HEIGHT*random.randint(1,self.HEIGHT)

        replace = 0
        fill = 3
        self.flood_fill(blueprint, x, 0, z, replace, fill)

        replace = 3
        fill = 4
        self.flood_fill(blueprint, x, height, z, replace, fill)

        for floor in range(-self.WALL_HEIGHT, 0, self.WALL_HEIGHT):

            for y in range(self.WALL_HEIGHT):
                for x in range(len(blueprint)):
                    for z in range(len(blueprint[x])):
                        if not blueprint[x][z] == 0:
                            self.draw_brick(x*self.BRICK_SIZE[0], y*self.BRICK_SIZE[1]+floor, z*self.BRICK_SIZE[2])


        for floor in range(0, height, self.WALL_HEIGHT):

            for y in range(self.WALL_HEIGHT):
                for x in range(len(blueprint)):
                    for z in range(len(blueprint[x])):
                        if blueprint[x][z] == 1:
                            self.draw_brick(x*self.BRICK_SIZE[0], y*self.BRICK_SIZE[1]+floor, z*self.BRICK_SIZE[2])
                        if blueprint[x][z] == 2:
                            if y < self.GLASS_HEIGHT[0] or y > self.GLASS_HEIGHT[1]:
                                self.draw_brick(x*self.BRICK_SIZE[0], y*self.BRICK_SIZE[1]+floor, z*self.BRICK_SIZE[2])


        for floor in range(0, height, self.WALL_HEIGHT):
            for y in range(self.WALL_HEIGHT):
                for x in range(len(blueprint)):
                    for z in range(len(blueprint[x])):    
                        if blueprint[x][z] == 2:
                            if y >= self.GLASS_HEIGHT[0] and y <= self.GLASS_HEIGHT[1]:
                                rotation = 1
                                if not x == 0 and not x+1 >= len(blueprint):
                                    if not blueprint[x-1][z] == 0 and not blueprint[x+1] == 0:
                                        rotation = 0
                                self.draw_glass(x*self.BRICK_SIZE[0], y*self.BRICK_SIZE[1]+floor, z*self.BRICK_SIZE[2], rotation)
                        
        glEndList()

        return callback

    def flood_fill(self, blueprint, x, y, z, replace, fill):
        self.draw_brick(x*self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z*self.BRICK_SIZE[2])
        blueprint[x][z] = fill

        if x-1 > 0 and blueprint[x-1][z] == replace:
            self.flood_fill(blueprint, x-1, y, z, replace, fill)
        if x+1 < len(blueprint) and blueprint[x+1][z] == replace:
            self.flood_fill(blueprint, x+1, y, z, replace, fill)
        if z-1 > 0 and blueprint[x][z-1] == replace:
            self.flood_fill(blueprint, x, y, z-1, replace, fill)
        if z+1 < len(blueprint[x]) and blueprint[x][z+1] == replace:
            self.flood_fill(blueprint, x, y, z+1, replace, fill)



    def draw_glass(self, x, y, z, rotation):
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.textures.applyTexture(self.glass)
        glColor4f(1,1,1,.5)
        self.draw_plane(x, y, z, rotation)
        glDisable(GL_BLEND)

    def draw_brick(self, x, y, z):
        self.textures.applyTexture(self.brick)
        glColor4f(1,1,1,1)
        self.draw_square(x, y, z)

    def draw_plane(self, x, y, z, rotation):
        glBegin(GL_QUADS)
        
        if rotation == 0:
        #front
            z -= self.BRICK_SIZE[2]/float(2)

            glTexCoord2f(0,1)
            glVertex3f(x, y, z)
            glTexCoord2f(1,1)
            glVertex3f(x+self.BRICK_SIZE[0], y, z)
            glTexCoord2f(1,0)
            glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z)
            glTexCoord2f(0,0)
            glVertex3f(x, y-self.BRICK_SIZE[1], z)

        else:
        #right
            x -= self.BRICK_SIZE[0]/float(2)
            
            glTexCoord2f(0,1)
            glVertex3f(x+self.BRICK_SIZE[0], y, z)
            glTexCoord2f(1,1)
            glVertex3f(x+self.BRICK_SIZE[0], y, z-self.BRICK_SIZE[2])
            glTexCoord2f(1,0)
            glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z-self.BRICK_SIZE[2])
            glTexCoord2f(0,0)
            glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z)
        
        glEnd()

    def draw_square(self, x, y, z):

        '''Draws back from top left front corner'''

        glBegin(GL_QUADS)
        
        #front
        glTexCoord2f(0,1)
        glVertex3f(x, y, z)
        glTexCoord2f(1,1)
        glVertex3f(x+self.BRICK_SIZE[0], y, z)
        glTexCoord2f(1,0)
        glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z)
        glTexCoord2f(0,0)
        glVertex3f(x, y-self.BRICK_SIZE[1], z)

        #top
        glVertex3f(x, y, z)
        glVertex3f(x, y, z-self.BRICK_SIZE[2])
        glVertex3f(x+self.BRICK_SIZE[0], y, z-self.BRICK_SIZE[2])
        glVertex3f(x+self.BRICK_SIZE[0], y, z)

        #left
        glTexCoord2f(1,1)
        glVertex3f(x, y, z)
        glTexCoord2f(0,1)
        glVertex3f(x, y, z-self.BRICK_SIZE[2])
        glTexCoord2f(0,0)
        glVertex3f(x, y-self.BRICK_SIZE[1], z-self.BRICK_SIZE[2])
        glTexCoord2f(1,0)
        glVertex3f(x, y-self.BRICK_SIZE[1], z)

        #right
        glTexCoord2f(0,1)
        glVertex3f(x+self.BRICK_SIZE[0], y, z)
        glTexCoord2f(1,1)
        glVertex3f(x+self.BRICK_SIZE[0], y, z-self.BRICK_SIZE[2])
        glTexCoord2f(1,0)
        glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z-self.BRICK_SIZE[2])
        glTexCoord2f(0,0)
        glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z)

        #back
        glTexCoord2f(1,1)
        glVertex3f(x, y, z-self.BRICK_SIZE[2])
        glTexCoord2f(0,1)
        glVertex3f(x+self.BRICK_SIZE[0], y, z-self.BRICK_SIZE[2])
        glTexCoord2f(0,0)
        glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z-self.BRICK_SIZE[2])
        glTexCoord2f(1,0)
        glVertex3f(x, y-self.BRICK_SIZE[1], z-self.BRICK_SIZE[2])

        #bottom
        glVertex3f(x, y-self.BRICK_SIZE[1], z)
        glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z)
        glVertex3f(x+self.BRICK_SIZE[0], y-self.BRICK_SIZE[1], z-self.BRICK_SIZE[2])
        glVertex3f(x, y-self.BRICK_SIZE[1], z-self.BRICK_SIZE[2])

        glEnd()

    def make_blueprint(self, x, z):
        blueprint = self.seed_blueprint(x,z)

        rooms = random.randint(self.ROOMS[0], self.ROOMS[1])
        room = self.make_room(blueprint, x/4, z/4)
        for i in range(rooms):

            quadrent = random.randint(1,4)
            overlap = (room[2]/random.uniform(self.OVERLAP[0], self.OVERLAP[1]), room[3]/random.uniform(self.OVERLAP[0], self.OVERLAP[1]))
            room_x = room[0]
            room_z = room[1]

            if quadrent == 1:
                room_x = room[0]+overlap[0]
                room_z = room[1]+overlap[1]
            elif quadrent == 2:
                room_x = (room[0]+room[2])-overlap[0]
                room_z = room[1]+overlap[1]
            elif quadrent == 3:
                room_x = (room[0]+room[2])-overlap[0]
                room_z = (room[1]+room[3])-overlap[1]
            elif quadrent == 1:
                room_x = room[0]+overlap[0]
                room_z = (room[1]+room[3])+overlap[1]

            room = self.make_room(blueprint, int(room_x), int(room_z))

        return blueprint

    def make_room(self, blueprint, x=0, z=0):
        size_x = random.randint(self.WALL_SIZE[0], self.WALL_SIZE[1])
        size_z = random.randint(self.WALL_SIZE[0], self.WALL_SIZE[1])

        for room_x in range(size_x+1):
            blueprint[room_x+x][z] = 1
            blueprint[room_x+x][size_z+z] = 1
        for room_z in range(size_z+1):
            blueprint[x][room_z+z] = 1
            blueprint[size_x+x][room_z+z] = 1

        return (x, z, size_x, size_z)
                
    def trace_blueprint(self, blueprint):
        blueprint_tmp = self.seed_blueprint(len(blueprint), len(blueprint[0]))
        origin = self.origin_blueprint(blueprint)
        
        direction_index = 'down'
        turtle = [origin[0], origin[1]]
        blueprint_tmp[turtle[0]][turtle[1]] = 1
        done = False

        while not done:
            direction_index = self.trace_move(blueprint, turtle, direction_index)
            move = self.move_turtle(direction_index)
            turtle[0] += move[0]
            turtle[1] += move[1]
            blueprint_tmp[turtle[0]][turtle[1]] = 1
            
            if turtle[0] == origin[0] and turtle[1] == origin[1]:
                done = True

        blueprint_tmp = self.trim_blueprint(blueprint_tmp)
            
        return blueprint_tmp


    def make_windows(self, blueprint):

        origin = self.origin_blueprint(blueprint)
        turtle = [origin[0], origin[1]]
        direction_index = 'down'
        counter = 0

        blueprint[turtle[0]][turtle[1]] = 1
        done = False

        while not done:

            direction_tmp = self.trace_move(blueprint, turtle, direction_index)
            
            if direction_tmp == direction_index:
                counter += 1
            else:

                if counter-2 >= self.WINDOW_SIZE[0]+(self.WINDOW_SIZE[1]*2):
                    self.add_windows(blueprint, turtle[:], counter, direction_index)
                counter = 0

            direction_index = direction_tmp
            
            move = self.move_turtle(direction_index)
            turtle[0] += move[0]
            turtle[1] += move[1]

            if turtle[0] == origin[0] and turtle[1] == origin[1]:
                self.add_windows(blueprint, turtle[:], counter, direction_index)
                done = True
        
        return blueprint

    def add_windows(self, blueprint, turtle_tmp, counter, direction_index):
        mod = int(math.floor(float(counter)/(self.WINDOW_SIZE[0]+self.WINDOW_SIZE[1])))
                    
        move_tmp = self.move_turtle(direction_index)
        move_tmp = [-move_tmp[0], -move_tmp[1]]
                                        
        pad = int(math.floor((counter-(mod*(self.WINDOW_SIZE[0]+self.WINDOW_SIZE[1])))/float(2)))
        
        for i in range(pad+1):
            turtle_tmp[0] += move_tmp[0]
            turtle_tmp[1] += move_tmp[1]

        for i in range(mod):
                        
            for j in range(self.WINDOW_SIZE[0]):
                turtle_tmp[0] += move_tmp[0]
                turtle_tmp[1] += move_tmp[1]
                blueprint[turtle_tmp[0]][turtle_tmp[1]] = 2
                            
            for j in range(self.WINDOW_SIZE[1]):
                turtle_tmp[0] += move_tmp[0]
                turtle_tmp[1] += move_tmp[1]


    def trace_move(self, blueprint, turtle, direction_index):

        x = turtle[0]
        z = turtle[1]
        
        if direction_index == 'down':
            if x-1 >= 0 and blueprint[x-1][z] == 1:
                direction_index = 'left'
            elif z+1 < len(blueprint[x]) and blueprint[x][z+1] == 1:
                direction_index = 'down'
            elif x+1 < len(blueprint) and blueprint[x+1][z] == 1:
                direction_index = 'right'
                    
        elif direction_index == 'right':
            if z+1 < len(blueprint[x]) and blueprint[x][z+1] == 1:
                direction_index = 'down'
            elif x+1 < len(blueprint) and blueprint[x+1][z] == 1:
                direction_index = 'right'
            elif z-1 >= 0 and blueprint[x][z-1] == 1:
                direction_index = 'up'

        elif direction_index == 'left':
            if z-1 >= 0 and blueprint[x][z-1] == 1:
                direction_index = 'up'
            elif x-1 >= 0 and blueprint[x-1][z] == 1:
                direction_index = 'left'
            elif z+1 < len(blueprint[x]) and blueprint[x][z+1] == 1:
                direction_index = 'down'
        
        elif direction_index == 'up':
            if x+1 < len(blueprint) and blueprint[x+1][z] == 1:
                direction_index = 'right'
            elif z-1 >= 0 and blueprint[x][z-1] == 1:
                direction_index = 'up'
            elif x-1 >= 0 and blueprint[x-1][z] == 1:
                direction_index = 'left'

        return direction_index
            


    def trim_blueprint(self, blueprint):
        x_trim = [1000,0]
        z_trim = [1000,0]
        for x in range(len(blueprint)):
            for z in range(len(blueprint[x])):
                if blueprint[x][z] == 1:
                    if x < x_trim[0]:
                        x_trim[0] = x
                    if x > x_trim[1]:
                        x_trim[1] = x
                    if z < z_trim[0]:
                        z_trim[0] = z
                    if z > z_trim[1]:
                        z_trim[1] = z
        
        blueprint_tmp = self.seed_blueprint(x_trim[1]-x_trim[0]+1, z_trim[1]-z_trim[0]+1)
        for x in range(x_trim[0], x_trim[1]+1):
            for z in range(z_trim[0], z_trim[1]+1):
                blueprint_tmp[x-x_trim[0]][z-z_trim[0]] = blueprint[x][z]

        return blueprint_tmp

    def origin_blueprint(self, blueprint):
        
        tmp_x = 200
        tmp_z = 200
        
        for z in range(len(blueprint[0])):
            for x in range(len(blueprint)):
                if blueprint[x][z] == 1 and x < tmp_x:
                    tmp_x = x
            for z in range(len(blueprint[tmp_x])):
                if blueprint[tmp_x][z] == 1 and z < tmp_z:
                    tmp_z = z
        return (tmp_x,tmp_z)
        
    def seed_blueprint(self, x, z):
        blueprint = []
        for i in range(x):
            blueprint.append([])
            for j in range(z):
                blueprint[i].append(0)
        return blueprint

    def move_turtle(self, _direction):
        move = [0,0]
        if _direction == 'down':
            move[1] += 1
        elif _direction == 'right':
            move[0] += 1
        elif _direction == 'left':
            move[0] -= 1
        elif _direction == 'up':
            move[1] -= 1
        return move

if __name__ == '__main__':
    s = Structure(TextureHolder(), None)
    s.create_structure()
    
            
        
