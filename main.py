#! /usr/bin/env python
from RenderWorld import RenderWorld
import sys, os

if __name__ == '__main__':
    RENDER = None
    if len(sys.argv) >= 2:
        for i in range(1, len(sys.argv)):
            if sys.argv[i].startswith('n'):
                os.system('rm data/textures/maps/*')
                print 'Removing maps'
            else:
                RENDER = RenderWorld(sys.argv[i])
    if RENDER == None:
        RENDER = RenderWorld(None)
