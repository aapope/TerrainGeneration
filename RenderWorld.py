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

class RenderWorld:
    '''This is the class that renders maze.
    Camera angles are handled by Camera.py.
    '''
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700
    SCALE = .5
    MAP_SIZE =100
    X_FACTOR = 1
    Y_FACTOR = 1
    Z_FACTOR = 1
    MAP_SIZE = 100
    SEA_LEVEL = 4

    def __init__(self, transaction):
        '''Sets up camera, modes, lighting, sounds, and objects.'''
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

    def create_render_newlist(self):
	self.need_lists = False	
	new_list = []
	for location, values in self.trans.location_var.items():
		print "RENDERING IN OPEN GL", location
		tex_file_name, face_norms, vert_norms, heights, offsetx, offsetz, textname, textid = values
		
		self.texture = self.tex_holder.hold_my_texture(tex_file_name, textname)

        	index = glGenLists(1)
		glNewList(index, GL_COMPILE)
        	self.tex_holder.applyTexture(self.texture)

        	for x in range(1, len(heights)):
            		glBegin(GL_TRIANGLE_STRIP)
            		for z in range(len(heights[x])):
               			glTexCoord2f(self.convert.convert('h', 'g', 'x', x)/float(self.convert.gl_x), self.convert.convert('h', 'g', 'z', -z)/float(self.convert.gl_z))

                		pt = (self.convert.convert('h', 'g', 'x', x+offsetx), heights[x][z], self.convert.convert('h','g','z',-(z+offsetz)))
				norm_point = (self.convert.convert('h', 'g', 'x', x), heights[x][z], self.convert.convert('h','g','z',-z))                		
				norm = vert_norms[norm_point]
                		glNormal3f(norm[0],norm[1],norm[2])
                		glVertex3f(pt[0],pt[1],pt[2])

                
                		glTexCoord2f(self.convert.convert('h', 'g', 'x', x-1)/float(self.convert.gl_x), self.convert.convert('h', 'g', 'z', -z)/float(self.convert.gl_z))

                		pt = (self.convert.convert('h', 'g', 'x', (x-1)+offsetx), heights[x-1][z], self.convert.convert('h','g','z',-(z+offsetz)))
				norm_point = (self.convert.convert('h', 'g', 'x', x-1), heights[x-1][z], self.convert.convert('h','g','z',-z))
                		norm = vert_norms[norm_point]
                		glNormal3f(norm[0],norm[1],norm[2])
                		glVertex3f(pt[0],pt[1],pt[2])
           		glEnd()
                

        	'''Water plane'''
        	self.tex_holder.applyTexture('water')
        	tile_size = self.tex_holder.images['water'].size
        	xlen = self.convert.gl_x
        	zlen = self.convert.gl_z
        	glBegin(GL_QUADS)
        	glTexCoord2f(0,0)
        	glVertex3f(0, self.convert.sea_level, 0)
        	glTexCoord2f(tile_size[0]/xlen,0)
        	glVertex3f(xlen, self.convert.sea_level, 0)
        	glTexCoord2f(tile_size[0]/xlen,tile_size[1]/zlen)
        	glVertex3f(xlen, self.convert.sea_level, -zlen)
        	glTexCoord2f(0,tile_size[1]/zlen)
        	glVertex3f(0, self.convert.sea_level, -zlen)
        	glEnd()

        	glEndList()
		
		new_list.append(index)
	 	'''
		filename = 'data/textures/texture'+textname+'.bmp'
		self.texture = self.loadTexture(filename, textid)		
		#load water
			
		self.texture = self.loadTexture(rend.run(heights, textname), textid)
		water = 'data/textures/water/water2.bmp'
		water_tex = self.loadTexture(water, 1)
	
		#create new genlist
		index = glGenLists(1)
		glNewList(index, GL_COMPILE)
	
		self.applyTexture(self.texture)
	
		z_incr = self.Z_FACTOR/float(len(heights))
		x_incr = self.X_FACTOR/float(len(heights[0]))
	
		#creates triangle list and applies texture
		for y in range(1, len(heights)):
		    glBegin(GL_TRIANGLE_STRIP)
		    for x in range(len(heights[y])):
		
			glTexCoord2f((len(heights)- y) * z_incr,-(x) * x_incr)
		        
			pt = ((x+offsetx)*self.X_FACTOR, heights[x][-y], -(y-1 + offsetz)*self.Z_FACTOR)
		        #norm = vert_norms[pt]
		        #glNormal3f(norm[0],norm[1],norm[2])
		        glVertex3f(pt[0],pt[1],pt[2])

			glTexCoord2f((len(heights)- y-1) * z_incr,-(x) * x_incr)
		        
			pt = ((x+offsetx)*self.X_FACTOR, heights[x][-y-1], -(y + offsetz)*self.Z_FACTOR)
		        #norm = vert_norms[pt]
		        #glNormal3f(norm[0],norm[1],norm[2])
		        glVertex3f(pt[0],pt[1],pt[2])
		    glEnd()
		glEndList()'''
		
	
	self.index_list = new_list
	#self.index_list = new_list
		
	'''
    #used to load a texture from a filename and apply it to triangles
    def loadTexture(self, filenames, texId):
        glGenTextures(1, texId)
        glBindTexture(GL_TEXTURE_2D, texId)
	images = []
        images.append(Image.open(filenames))
        glTexImage2D(GL_TEXTURE_2D, 0, 3, images[-1].size[0], images[-1].size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, images[-1].tostring("raw","RGBX",0,-1))
        return texId

    #used to apply texture used a textID
    def applyTexture(self, tex_id):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)'''

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
        #glEnable(GL_DEPTH_TEST)

        glEnable(GL_FOG)
        glFogi (GL_FOG_MODE, GL_EXP2)
        glFogfv (GL_FOG_COLOR, (.8,.8,.8,1))
        glFogf (GL_FOG_DENSITY, .0004)
        glHint (GL_FOG_HINT, GL_NICEST)
    
    def renderLightSource(self):
        '''Resets the light sources to the right position.'''
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)

    def set_up_lighting(self):
        self.diffuse_pos1 = (0,.5,-1,0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)

        
        glLightfv(GL_LIGHT1, GL_AMBIENT, (1, 1, 1, .95))
        glLightfv(GL_LIGHT1, GL_POSITION, (1,1,1,1))

    def set_up_convert(self):
        #heightmap, texture, gl
        self.convert = Convert((1, 1, 1), (10, 1, 10), (1*self.SCALE, 35*self.SCALE, 1*self.SCALE))
        

    def load_map(self, heightmap_filename):
        self.load = LoadTerrain(heightmap_filename, self.convert, self.tex_holder)
        self.heights = self.load.load()
        self.map_index = self.load.createRenderList(self.heights)

    def load_skybox(self):
        #self.skybox = Skybox((len(self.heights[0])*self.X_FACTOR, self.Y_FACTOR, len(self.heights)*self.Z_FACTOR))
        map_length = self.convert.open_gl_scale
        self.skybox = Skybox((5000,5000,5000))
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
        
	self.renderLightSource()
	

	for index in self.index_list:
		#print "INDEX:", index
		glCallList(index)
	

        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        #glCallList(self.index)
        
        glDisable(GL_LIGHTING)
        glLoadIdentity()
	
	
        glTranslate(-self.skybox.x/2, -self.camera.pos_Y, -self.skybox.z/2)
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
        elif key == 'x':
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
'''
if __name__ == '__main__':
    if len(sys.argv) == 0:
        RENDER = RenderWorld(sys.argv[1])
    else:
        RENDER = RenderWorld(None)'''
