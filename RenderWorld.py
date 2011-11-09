'''Contains a class that renders the maze itself.'''

__author__ = "Emily and Andrew"
__date__ = "21 October 2011"

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Image
from Camera import Camera
from LoadTerrain import LoadTerrain
from Skybox import Skybox

class RenderWorld:
    '''This is the class that renders maze.
    Camera angles are handled by Camera.py.
    '''
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700
    X_FACTOR = 10
    Y_FACTOR = 350
    Z_FACTOR = 10
    MAP_SIZE = 100

    def __init__(self, filename):
        '''Sets up camera, modes, lighting, sounds, and objects.'''
        self.set_up_graphics()
        self.set_up_lighting()
        self.camera = Camera(0,20,0)
        self.poly_view = False

        glutIdleFunc(self.display)
        glutDisplayFunc(self.display)

        glutIgnoreKeyRepeat(GLUT_KEY_REPEAT_OFF)
        glutKeyboardFunc(self.keyPressed)
        glutKeyboardUpFunc(self.keyUp)

        glutSetCursor(GLUT_CURSOR_NONE)
        glutPassiveMotionFunc(self.mouseMove)

        if not filename == None:
            self.load = LoadTerrain(filename, (self.X_FACTOR, self.Y_FACTOR, self.Z_FACTOR))
        else:
            self.load = LoadTerrain('data/heightmaps/fractal.bmp',  (self.X_FACTOR, self.Y_FACTOR, self.Z_FACTOR))
        self.heights = self.load.load()
        self.index = self.load.createRenderList(self.heights)
        
        #self.skybox = Skybox((len(self.heights[0])*self.X_FACTOR, self.Y_FACTOR, len(self.heights)*self.Z_FACTOR))
        self.skybox = Skybox((5000, 5000, 5000))
        self.sky_index = self.skybox.createCallList(1, 3)
        
        glutMainLoop()

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

    def set_up_lighting(self):
        self.diffuse_pos1 = (0,.5,-1,0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)

        
        glLightfv(GL_LIGHT1, GL_AMBIENT, (1, 1, 1, .95))
        glLightfv(GL_LIGHT1, GL_POSITION, (1,1,1,1))
        
        
        

    def display(self, x=0, y=0):
        '''Called for every refresh; redraws the floor and objects
        based on the camera angle. Calls collision detection, handles
        the appropriate objects for keys, doors, etc.'''
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()
        
        self.camera.move()
        self.camera.renderRotateCamera()
        self.camera.renderTranslateCamera()
        self.renderLightSource()
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        
        glCallList(self.index)
        
        glDisable(GL_LIGHTING)
        
        glLoadIdentity()
        
        self.camera.renderRotateCamera()
        glTranslate(-self.skybox.x/2, -self.camera.pos_Y, -self.skybox.z/2)
        glCallList(self.sky_index)
        
        glDisable(GL_TEXTURE_2D)

        
        glutSwapBuffers()

    def renderLightSource(self):
        '''Resets the light sources to the right position.'''
        glLightfv(GL_LIGHT0, GL_POSITION, self.diffuse_pos1)

       
    def mouseMove(self, x, y):
        '''Called when the mouse is moved.'''
        factor = 2
        
        tmp_x = (self.camera.mouse_x - x)/factor
        tmp_y = (self.camera.mouse_y - y)/factor
        if tmp_x > self.camera.ROTATE:
            tmp_x = self.camera.ROTATE
        elif tmp_x < -self.camera.ROTATE:
            tmp_x = -self.camera.ROTATE
        if tmp_y > self.camera.ROTATE:
            tmp_y = self.camera.ROTATE
        elif tmp_y < -self.camera.ROTATE:
            tmp_y = -self.camera.ROTATE

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
        if key == 'x' and not self.poly_view:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            self.poly_view = True
        elif key == 'x' and self.poly_view:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self.poly_view = False
        if key == 'p':
            exit(0)
        if key.lower() == 'q':
            self.camera.WALK += .1
            self.camera.SPRINT += .5
        if key.lower() == 'e':
            self.camera.WALK -= .1
            self.camera.SPRINT -= .5

    def keyUp(self, key, x, y):
        '''Called when a key is released.'''
        self.camera.keys[key.lower()] = False
        if not glutGetModifiers() == GLUT_ACTIVE_SHIFT:
            self.camera.keys["shift"] = False

if __name__ == '__main__':
    if len(sys.argv) == 0:
        RENDER = RenderWorld(sys.argv[1])
    else:
        RENDER = RenderWorld(None)
