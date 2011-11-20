'''Contains a class that doesnt renders the maze itself.'''
__author__ = "Andrew, Jordan, Sam"
__date__ = "10 November 2011"


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Image
from Camera import Camera
from LoadTerrain import LoadTerrain
from World import World
from Skybox import Skybox
from Convert import Convert
from TextureHolder import TextureHolder
import threading

CONFIG = "constants.conf"
HEIGHT_SCALE = 8


class RenderWorld:
    '''This is the class that renders maze.
    Camera angles are handled by Camera.py.
    '''
    
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700
    SCALE = 1
    X_FACTOR = 1
    Y_FACTOR = 1
    Z_FACTOR = 1
    SEA_LEVEL = 4

    def __init__(self, transaction):
        '''Sets up camera, modes, lighting, sounds, and objects.'''
        f = open(CONFIG)
        lines = f.read().split("\n")
        self.QUALITY = int(lines[0].split()[1])
        self.MAP_SIZE = int(lines[1].split()[1])
        self.SKYBOX_SIZE = float(lines[2].split()[1])/3
        self.HEIGHT_SCALE = int(float(lines[3].split()[1])*self.MAP_SIZE)
        f.close()
        
        self.set_up_convert()
        self.tex_holder = TextureHolder()
        self.index_list = []
        self.lock = threading.RLock()
        self.need_lists = False
        
        self.trans = transaction
        #self.skybox = Skybox((5000, 5000, 5000))
        #self.sky_index = self.skybox.createCallList(1, 3)
        #self.skybox = Skybox((len(self.heights[0])*self.X_FACTOR, self.Y_FACTOR, len(self.heights)*self.Z_FACTOR))
               
    def set_up(self):
        self.set_up_graphics()
        self.set_up_lighting()
        self.set_up_glut()
        water_path = 'data/textures/water/water.bmp'
        self.tex_holder.hold_my_texture(water_path, 'water')        
        self.camera = Camera(10,20,-10)
        
        self.poly_view = False
        self.load_skybox()


    def set_up_glut(self):
        glutIdleFunc(self.display)
        glutDisplayFunc(self.display)

        glutIgnoreKeyRepeat(GLUT_KEY_REPEAT_OFF)
        glutKeyboardFunc(self.keyPressed)
        glutKeyboardUpFunc(self.keyUp)

        glutSetCursor(GLUT_CURSOR_NONE)
        glutPassiveMotionFunc(self.mouseMove)
        
        #glGenLists(50)
        #glNewList(1, GL_COMPILE)
        #glNewList(1, GL_COMPILE)
    
    def start_loop(self):
        glutMainLoop()

    def to_gl(self, axis, oldnum):
        if axis == 'x':
            return self.convert.convert_for_triangle('x', oldnum)
        else:
            return self.convert.convert_for_triangle('z', oldnum)

    def create_render_newlist(self):
        self.need_lists = False
        new_list = []
        #print "trying to render"
        #print self.trans.location_var
        for location, values in self.trans.location_var.items():
            #print "RENDERING IN OPEN GL", location
            tex_file_name, face_norms, vert_norms, heights, offsetx, offsetz, textname, textid = values
            #print vert_norms

            self.texture = self.tex_holder.hold_my_texture(tex_file_name, textname)
    
            #offsetx *= .999
            #offsetz *= .999 
            index = glGenLists(1)
            glNewList(index, GL_COMPILE)
            #print "new texture applied"
            self.tex_holder.applyTexture(self.texture)
            zdivide = float(self.MAP_SIZE)
            xdivide = float(self.MAP_SIZE+1)
            #go by rows
            for z in range(len(heights)-1):
                glBegin(GL_TRIANGLE_STRIP)
                for x in range(len(heights[z])):
                    #start at (0,1)
                    point1x = self.to_gl('x', x)    #first point x value in opengl coordinate
                    point1z = self.to_gl('z', z+1)  #first point z value in opengl coordinate

                    glTexCoord2f(point1x/xdivide, -point1z/zdivide)
                    #print "f1:", point1x/divide, "f2:", -point1z/divide

                    pt = (point1x+offsetx, heights[x][z+1], point1z-offsetz)
                    m_point = (point1x, heights[x][z+1], point1z)
                    norm = vert_norms[m_point]
                    glNormal3f(norm[0],norm[1],norm[2])
                    glVertex3f(pt[0],pt[1],pt[2])
                    #############################################
                    #second point (0,0)

                    point2x = self.to_gl('x',x)     #second point x value in opengl coordinate
                    point2z = self.to_gl('z',z)     #second point z value in opengl coordinate
                    
                    glTexCoord2f(point2x/xdivide, -point2z/zdivide)
                    #print "f1:", point2x/divide, "f2:", -point2z/divide

                    pt = (point2x+offsetx, heights[x][z], point2z-offsetz)
                    m_point = (point2x, heights[x][z], point2z)
                    norm = vert_norms[m_point]
                    glNormal3f(norm[0],norm[1],norm[2])
                    glVertex3f(pt[0],pt[1],pt[2])
                    
                glEnd()
            #print z

            '''Water plane'''
            glDisable(GL_LIGHTING)
        

            self.tex_holder.applyTexture('water')
            tile_size = self.tex_holder.images['water'].size
            
            xlen = float(self.convert.gl_x)
            zlen = float(self.convert.gl_z)
            glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glEnable (GL_BLEND)
            glColor4f(1,1,1,.5)
            glBegin(GL_QUADS)

            glTexCoord2f(0, 0)
            glVertex3f(0+offsetx, self.convert.sea_level, 0-offsetz)

            glTexCoord2f(tile_size[0]/xlen/10, 0)
            glVertex3f(xlen+offsetx, self.convert.sea_level, 0-offsetz)

            glTexCoord2f(tile_size[0]/xlen/10, tile_size[1]/zlen/10)
            glVertex3f(xlen+offsetx, self.convert.sea_level, -zlen-offsetz)

            glTexCoord2f(0, tile_size[1]/zlen/10)
            glVertex3f(0+offsetx, self.convert.sea_level, -zlen-offsetz)
            glEnd()
            glDisable(GL_BLEND)
            glEnable(GL_LIGHTING)

            glEndList()
            
            new_list.append(index)


        self.index_list = new_list
        #self.index_list = new_list

    def set_up_graphics(self):
        '''Sets up OpenGL to provide double buffering, RGB coloring,
        depth testing, the correct window size, perspective
        rendering/fulcrum clipping, and a title.'''
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glutCreateWindow('Terrains!')

        glMatrixMode(GL_PROJECTION)

        gluPerspective(45,1,.1,8000)
        glMatrixMode(GL_MODELVIEW)

        #glClearColor(.529,.8078,.980,0)
        glEnable(GL_NORMALIZE)

        glEnable (GL_DEPTH_TEST)

        glShadeModel(GL_SMOOTH)
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glEnable(GL_FOG)
        glFogi (GL_FOG_MODE, GL_EXP2)
        glFogfv (GL_FOG_COLOR, (.8,.8,.8,1))
        glFogf (GL_FOG_DENSITY, .02)
        glHint (GL_FOG_HINT, GL_FASTEST)
    
    def renderLightSource(self):
        '''Resets the light sources to the right position.'''
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)

    def set_up_lighting(self):
        self.diffuse_pos1 = (0,.5,-1,0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)

        
        glLightfv(GL_LIGHT1, GL_AMBIENT, (1, 1, 1, .5))
        glLightfv(GL_LIGHT1, GL_POSITION, (1,1,1,1))

    def set_up_convert(self):
        #heightmap, texture, gl
        self.convert = Convert((1, 1, 1), (self.QUALITY, 1, self.QUALITY), (1*self.SCALE, self.HEIGHT_SCALE*self.SCALE, 1*self.SCALE), self.MAP_SIZE)
        

    def load_map(self, heightmap_filename):
        self.load = LoadTerrain(heightmap_filename, self.convert, self.tex_holder)
        self.heights = self.load.load()
        self.map_index = self.load.createRenderList(self.heights)

    def load_skybox(self):
        #self.skybox = Skybox((len(self.heights[0])*self.X_FACTOR, self.Y_FACTOR, len(self.heights)*self.Z_FACTOR))
        scale = (self.convert.gl_x+self.convert.gl_z)*self.SKYBOX_SIZE
        self.skybox = Skybox(self.tex_holder, (scale,scale,scale))
        self.sky_index = self.skybox.createCallList(1, 3)

    def display(self, x=0, y=0):
        '''Called for every refresh; redraws the floor and objects
        based on the camera angle. Calls collision detection, handles
        the appropriate objects for keys, doors, etc.'''
        #print "loopdy loop"
        if self.need_lists:
            self.create_render_newlist()

            #self.lock.acquire()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        #Put camera and light in the correct position
        self.camera.move()
        self.camera.renderRotateCamera()
        self.camera.renderTranslateCamera()

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        self.renderLightSource()

        for index in self.index_list:
            #print "INDEX:", index
            glCallList(index)
        

        glLoadIdentity()        
        glDisable(GL_LIGHTING)
        self.camera.renderRotateCamera()
        glTranslate(-self.skybox.x/2, -1-self.camera.pos_Y, -self.skybox.z/2)
        glCallList(self.sky_index)    
        
        glDisable(GL_TEXTURE_2D)
        glutSwapBuffers()

    def renderLightSource(self):
        '''Resets the light sources to the right position.'''
        if self.camera.pos_Y <= self.convert.sea_level:
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (0, .2, 1, 1))
        else:
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)

       
    def mouseMove(self, x, y):
        '''Called when the mouse is moved.'''
        factor = 2
        
        tmp_x = (self.camera.mouse_x - x)/factor
        tmp_y = (self.camera.mouse_y - y)/factor
        if tmp_x > self.camera.ROTATE:
            tmp_x = self.camera.ROTATE
        self.camera.rotate(tmp_y, tmp_x, 0)
        x = self.WINDOW_WIDTH/2
        y = self.WINDOW_HEIGHT/2
        glutWarpPointer(x, y)
        self.camera.mouse_x = x
        self.camera.mouse_y = y
        
    def keyPressed(self, key, x, y):
        '''Called when a key is pressed.'''
        if key.lower() in self.camera.keys:
            self.camera.keys[key.lower()] = True
        if glutGetModifiers() == GLUT_ACTIVE_SHIFT:
            self.camera.keys["shift"] = True
        if key == 'p' and not self.poly_view:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            self.poly_view = True
        elif key == 'p' and self.poly_view:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self.poly_view = False
        elif key == 't':
            exit(0)
        if key.lower() == 'q':
            self.camera.WALK *= 1.2
            self.camera.SPRINT *= 1.2
        if key.lower() == 'e':
            self.camera.WALK *= .8
            self.camera.SPRINT *= .8

    def keyUp(self, key, x, y):
        '''Called when a key is released.'''
        self.camera.keys[key.lower()] = False
        if not glutGetModifiers() == GLUT_ACTIVE_SHIFT:
            self.camera.keys["shift"] = False
