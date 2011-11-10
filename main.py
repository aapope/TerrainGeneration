#! /usr/bin/env python
from RenderWorld import RenderWorld
import sys
import threading
from World import World
from RenderWorld import RenderWorld
from ThreadTransaction import ThreadTransaction

if __name__ == '__main__':
    if len(sys.argv) == 2:
	pass
        #RENDER = RenderWorld(sys.argv[1])
    else:
	trans = ThreadTransaction()
	r = RenderWorld(trans)
	w = World(r, trans)	
	
	w.create_world()
	r.set_up()	
	
	background_thread = threading.Thread(target=w.start)
	#graphic_thread = threading.Thread(target=r.start_loop)
	
	background_thread.start()
	r.start_loop()

	
	#graphic_thread.start()

        #RENDER = RenderWorld(None)
