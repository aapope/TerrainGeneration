from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import Image
import sys
import math
import time
import random

from Terrain import Terrain
from camera import *

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
MOVEMENT_SPEED = .2

class GameEngine:


    def __init__(self):
        self.key_down = [False] * 256
        self.myCamera = Camera(rX = 0, pX = 0, pY = 20.5, pZ = 5)
        self.current_time = time.time()
        self.frame_count = 0


        self.openGLInit()
        self.terrain = Terrain()
        self.terrain.load("fractal_small.bmp")
        self.run()



    def keyPressed(self, key, x, y):
        self.key_down[ord(key)] = True

    def keyReleased(self, key, x, y):
        self.key_down[ord(key)] = False


    def checkKeypresses(self):
        if self.key_down[ord('w')]:
            self.myCamera.moveForward(MOVEMENT_SPEED)
        if self.key_down[ord('a')]:
            self.myCamera.strafeLeft(MOVEMENT_SPEED)
        if self.key_down[ord('s')]:
            self.myCamera.moveBackward(MOVEMENT_SPEED)
        if self.key_down[ord('d')]:
            self.myCamera.strafeRight(MOVEMENT_SPEED)
        if self.key_down[ord('c')]:
            self.myCamera.diveDown(MOVEMENT_SPEED)
        if self.key_down[ord(' ')]:
            self.myCamera.flyUp(MOVEMENT_SPEED)
        if self.key_down[ord('x')]:
            sys.exit(1)


    def mouseMoved(self, x, y):
        self.myCamera.look(x, y)



    def openGLInit(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        glutCreateWindow("Terrain Generator")

        glClearColor(1, 1, 1, 1)

        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45., 1., .1, 1500.)
        glMatrixMode(GL_MODELVIEW)
        glShadeModel(GL_SMOOTH)
        glutKeyboardFunc(self.keyPressed)
        glutKeyboardUpFunc(self.keyReleased)
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        #glEnable(GL_CULL_FACE)
        #glutMotionFunc(self.mouseMoved)
        glutPassiveMotionFunc(self.mouseMoved)
        # glutSetKeyRepeat(GLUT_KEY_REPEAT_OFF)
        glutSetCursor(GLUT_CURSOR_NONE)


        # glEnable(GL_LIGHTING)
        # lightZeroPosition = [50, 40, 50, 0]
        # lightZeroColor = [.5, 1, .1, 0.0]
        # glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
        # glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
        # glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        # glEnable(GL_LIGHT0)

        # light_ambient = (1, 1, 1, 1)
        # light_position = (10, 50, 0, 0)
        # glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
        # glLightfv(GL_LIGHT1, GL_POSITION, light_position)

        #glEnable(GL_LIGHT1)



    def run(self):
        glutMainLoop()


    def calculateFPS(self):
        elapsed_time = time.time() - self.current_time
        if elapsed_time > 0:
            return "FPS: %.2f" % (self.frame_count / elapsed_time)
        self.current_time = time.time()
        self.frame_count = 0

    def display(self):
        self.frame_count += 1

        self.checkKeypresses()

        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        self.myCamera.render()
        self.terrain.render()
        #self.terrain.optimizedRender()

        glColor3f(1, 0, 0)
        glWindowPos2i(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50)

        fps = self.calculateFPS()
        glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, fps)

        glutSwapBuffers()


if __name__ == '__main__': 
	engine = GameEngine()


