from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys, math


MOUSEVIEW_RATIO = 0.1

class Camera:

    def __init__(self, rX=0, rY=0, rZ=0, pX=0, pY=0, pZ=0):
        self.rotateX = rX
        self.rotateY = rY
        self.rotateZ = rZ
        self.positionX = pX
        self.positionY = pY
        self.positionZ = pZ

        self.lastX = 0
        self.lastY = 0



    def diveDown(self, amount):
        self.positionY -= amount

    def flyUp(self, amount):
        self.positionY += amount

    def moveForward(self, amount):
        #yrotrad = (self.rotateY / 180 * math.pi);
        #self.positionX -= math.sin(yrotrad) * 0.2
        #self.positionZ -= math.cos(yrotrad) * 0.2

        yrotrad = -(self.rotateY / 180 * math.pi)
        xrotrad = -(self.rotateX / 180 * math.pi)
        self.positionX += math.sin(yrotrad) * amount
        self.positionZ -= math.cos(yrotrad) * amount
        #self.positionY -= math.sin(xrotrad) * amount


    def moveBackward(self, amount):
        #self.positionX = 0
        #yrotrad = (self.rotateY / 180 * math.pi)
        #self.positionX += math.sin(yrotrad) * 0.2
        #self.positionZ += math.cos(yrotrad) * 0.2
        #self.positionZ += amount

        yrotrad = -(self.rotateY / 180 * math.pi)
        xrotrad = -(self.rotateX / 180 * math.pi)
        self.positionX -= math.sin(yrotrad) * amount
        self.positionZ += math.cos(yrotrad) * amount
        #self.positionY += math.sin(xrotrad) * amount

    def strafeLeft(self, amount):
        yrotrad = -(self.rotateY / 180 * math.pi)
        self.positionX -= math.cos(yrotrad) * amount
        self.positionZ -= math.sin(yrotrad) * amount
        #self.positionX -= amount

    def strafeRight(self, amount):
        yrotrad = -(self.rotateY / 180 * math.pi)
        self.positionX += math.cos(yrotrad) * amount
        self.positionZ += math.sin(yrotrad) * amount
        #self.positionX += amount


    def look(self, x, y):
        if self.lastY != 0 and self.lastX != 0:
            diffx = x - self.lastX
            diffy = y - self.lastY
            self.lastX = x
            self.lastY = y
            self.rotateX += diffy * MOUSEVIEW_RATIO
            self.rotateY -= diffx * MOUSEVIEW_RATIO
        else:
            self.lastX = x
            self.lastY = y

        self.checkMouseWarp(x, y)

        #if self.rotateY > 360 or self.rotateY < -360:
        #    self.rotateY = self.rotateY % 360
        #if self.rotateX > 360 or self.rotateX < -360:
        #    self.rotateX = self.rotateX % 360


    def checkMouseWarp(self, x, y):
        if x > 300 or x < 100:
            x = 200
            glutWarpPointer(x, y)
            self.lastX = 0
            self.lastY = 0
        if y > 300 or y < 100:
            y = 200
            glutWarpPointer(x, y)
            self.lastX = 0
            self.lastY = 0

        

        #self.rotateZ = angleX
        #self.rotateY = angleY

    def __str__(self):
        position = "posX=%d, posY=%d, posZ=%d\n" % (self.positionX, self.positionY, self.positionZ)
        rotation = "rotX=%d, rotY=%d, rotZ=%d\n" % (self.rotateX, self.rotateY, self.rotateZ)
        return position + rotation

    def render(self):
        #print self
        glRotatef(-self.rotateX , 1.0, 0.0, 0.0)
        glRotatef(-self.rotateY , 0.0, 1.0, 0.0)
        glRotatef(-self.rotateZ , 0.0, 0.0, 1.0)
        glTranslatef(-self.positionX, -self.positionY, -self.positionZ )





