'''Contains a class that renders the maze itself.'''

__author__ = "Emily and Andrew"
__date__ = "21 October 2011"

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Camera import Camera
from LoadTerrain import LoadTerrain

class RenderWorld:
    '''This is the class that renders maze.
    Camera angles are handled by Camera.py.
    '''
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 700
    MAP_SIZE =100

    def __init__(self):
        '''Sets up camera, modes, lighting, sounds, and objects.'''
        self.set_up_graphics()
        self.camera = Camera(0,0,0)

        glutIdleFunc(self.display)
        glutDisplayFunc(self.display)

        glutIgnoreKeyRepeat(GLUT_KEY_REPEAT_OFF)
        glutKeyboardFunc(self.keyPressed)
        glutKeyboardUpFunc(self.keyUp)

        glutSetCursor(GLUT_CURSOR_NONE)
        glutPassiveMotionFunc(self.mouseMove)

        load = LoadTerrain('matthew/fractal.bmp')
        load.createRenderList(load.load())
        
        glutMainLoop()

    def set_up_graphics(self):
        '''Sets up OpenGL to provide double buffering, RGB coloring,
        depth testing, the correct window size, perspective
        rendering/fulcrum clipping, and a title.'''
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glutCreateWindow('Mazeworld!')

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45,1,.15,100)
        glMatrixMode(GL_MODELVIEW)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glEnable(GL_DEPTH_TEST)

    def display(self, x=0, y=0):
        '''Called for every refresh; redraws the floor and objects
        based on the camera angle. Calls collision detection, handles
        the appropriate objects for keys, doors, etc.'''
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.camera.move()
        self.camera.renderCamera()
        glCallList(1)
        glutSwapBuffers()
       
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
        if key == 'j':
            self.camera.rotate(0,3,0)
        elif key == 'l':
            self.camera.rotate(0,-3,0)
        elif key == 'i':
            self.camera.rotate(3,0,0)
        elif key == 'k':
            self.camera.rotate(-3,0,0)
        elif key == ' ':
            self.camera.pos_Y += .1
        elif key == 'c':
            self.camera.pos_Y -= .1
        elif key == 'x':
            exit(0)

    def keyUp(self, key, x, y):
        '''Called when a key is released.'''
        # Speed things up by not checking if the key is in the map
        self.camera.keys[key.lower()] = False
        if not glutGetModifiers() == GLUT_ACTIVE_SHIFT:
            self.camera.keys["shift"] = False

if __name__ == '__main__':
    RENDER = RenderWorld()
