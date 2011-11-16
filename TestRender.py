'''Contains a class that doesnt renders the maze itself.'''

__author__ = "Andrew, Jordan, Sam"
__date__ = "10 November 2011"


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Camera import Camera
from Structure import Structure

class TestRender:
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

    def __init__(self):
        self.set_up_graphics()
        self.load_object()
	self.set_up_glut()
        self.camera = Camera(0,60,0)
	self.camera.rotate(-75,-150,0)
	self.poly_view = False	
        self.start_loop()


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

    def set_up_graphics(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        glutCreateWindow('Terrains!')

        glMatrixMode(GL_PROJECTION)

        gluPerspective(45,1,.1,500)
        glMatrixMode(GL_MODELVIEW)

        #glClearColor(.529,.8078,.980,0)
        glEnable(GL_NORMALIZE)

        glEnable (GL_DEPTH_TEST)

        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    def load_object(self):
        self.load = Structure()
        self.structure = self.load.create_structure()

    def display(self, x=0, y=0):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        #Put camera and light in the correct position
        self.camera.move()
	self.camera.renderRotateCamera()
        self.camera.renderTranslateCamera()
        glCallList(self.structure)
	
        
        glDisable(GL_TEXTURE_2D)
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

if __name__ == '__main__':
    RENDER = TestRender()
