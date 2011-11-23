#! /usr/bin/env python

import sys
import os
import threading
from World import World
from RenderWorld import RenderWorld
from ThreadTransaction import ThreadTransaction

if __name__ == '__main__':
    if len(sys.argv) == 2:
        for i in range(1, len(sys.argv)):
            if sys.argv[i].startswith('n'):
                os.system('rm data/textures/maps/*')
                os.system('rm data/heightmaps/maps/*')
                print 'Removing maps'
                trans = ThreadTransaction()
                r = RenderWorld(trans)
                w = World(r, trans, False)	
                w.create_world()
                r.set_up()     
                background_thread = threading.Thread(target=w.start)
                background_thread.start()
                r.start_loop()

            elif sys.argv[i].startswith('i'):
                os.system('rm data/textures/maps/*')
                os.system('rm data/heightmaps/maps/*')
                
                trans = ThreadTransaction()
                r = RenderWorld(trans)
                w = World(r, trans, True)	
                w.create_world()
                r.set_up()     
                background_thread = threading.Thread(target=w.start)
                background_thread.start()
                r.start_loop()
                
    else:
        trans = ThreadTransaction()
        r = RenderWorld(trans)
        w = World(r, trans, True)	
    
        w.create_world()
        r.set_up()	
    
        background_thread = threading.Thread(target=w.start)
	#graphic_thread = threading.Thread(target=r.start_loop)
	
        background_thread.start()
        r.start_loop()

	
	#graphic_thread.start()

        #RENDER = RenderWorld(None)
