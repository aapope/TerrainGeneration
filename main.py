#! /usr/bin/env python
from RenderWorld import RenderWorld
import sys
import threading
from World import World
from RenderWorld import RenderWorld

if __name__ == '__main__':
    if len(sys.argv) == 2:
	pass
        #RENDER = RenderWorld(sys.argv[1])
    else:
	
	r = RenderWorld(None)
	w = World(r)
	background_thread = threading.Thread(target=w.create_world)
	graphic_thread = threading.Thread(target=r.set_up)

	background_thread.start()
	graphic_thread.start()

        #RENDER = RenderWorld(None)
