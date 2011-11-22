#class to control background

XFACTOR = 1
YFACTOR = 25
ZFACTOR = 1

CONFIG = "constants.conf"

from DiamondSquare import DiamondSquare
from LoadTerrain import LoadTerrain
import threading
#import Queue
import time
import copy
from multiprocessing import Process, JoinableQueue, Queue, Pipe
#from RenderThread import RenderThread

PATH = "data/heightmaps/maps/"

class World:
	

	def __init__(self, rw, transaction):
		f = open(CONFIG)
		lines = f.read().split("\n")
		self.OFFSET = int(lines[1].split()[1])
		self.size = int(lines[2].split()[1])			
		self.FACTOR = int(self.size)/2
		print self.size, self.FACTOR
		f.close()		

		self.rw = rw
		#self.size = 5
		self.curr_x = 0
		self.curr_y = 0
		self.diamonds = {}
		self.index_list = []
		self.pos_list = []
		self.total_terr = 1
		self.trans = transaction
		self.temp_dic = {}
		
		
		#self.text_holder = TextureHolder()
		
	#used to create the inital world
	def create_world(self):
		#self.init_world()
		self.rw.index_list = []
		self.initalize = True
		nlist = self.create_lists([], (0,0))	
		self.rw.lock.acquire()
		self.rw.index_list = nlist
		self.rw.lock.release()
		

	def start(self):	
		while True:
			self.update_loc(self.rw.camera.pos_X, self.rw.camera.pos_Y, self.rw.camera.pos_Z)
			#print "inside thread"
			time.sleep(1)
	
	#Used to create the inital world
	def init_world(self):
		for y in range(-self.FACTOR, self.size-self.FACTOR):
			for x in range(-self.FACTOR, self.size-self.FACTOR):
				#print "POS:",x,y
				self.pos_list.append((x,y))				
				ds = DiamondSquare((x, y), (self.OFFSET+1, self.OFFSET+1))
				ds.diamond_square_tile(self.diamonds)
				self.diamonds[(x,y)] = ds
				#if (not x == 1 and not y == -1):
					#if (not x == 0 and not y == 0):
						#if (not x == -1 and not y == 1):# or (not x == 1 and not y == -1):
				ds.save(PATH+str(x)+"_"+str(y)+".bmp")
	
	#Used to update camera location
	def update_loc(self,x,y,z):
		#print str(x),",",str(y)+",", str(z)
		x = int(x)
		z = int(z)
		if not self.is_in_tile(x,z,self.curr_x, self.curr_y):		
			newloc = self.get_tile(x,y,z)			
			self.curr_x = newloc[0]
			self.curr_y = newloc[1]
			print "NEWLOC:", newloc
			self.update_diamonds(newloc)

	def get_tile(self, x,y,z):
		x=int(x)
		y=int(y)
		z=int(z)
		for loc in self.pos_list:
				posx, posy = loc
				#print "POS:", posx, posy
				#print "stuff:",x,z,posx,posy
				if self.is_in_tile(x,z,posx,posy):
					return loc

	def is_in_tile(self,x,z,posx, posy):
	
		if posy < 0:
			if x in range(posx*self.OFFSET, (posx+1)*(self.OFFSET)) and z in range((posy)*(self.OFFSET), (posy-1)*self.OFFSET, -1):
				return True
			else:
				return False
		else:
			if x in range(posx*self.OFFSET, (posx+1)*(self.OFFSET)) and z in range((posy-1)*(self.OFFSET), (posy)*self.OFFSET):
				return True
			else:
				return False
		
	#Used to update the world list
	def update_diamonds(self, new_loc):
		x,y = new_loc
		copy_list = copy.deepcopy(self.pos_list)
		
		
		print "creating lists"
		self.create_lists(copy_list, new_loc)
		
	def render_thing(self, que, resp_que, init, new_loc, offset, factor):
		from TextureHolder import TextureHolder
		h_range = (200, 255)
		#create new heightmaps
		nwlx, nwly = new_loc
		diamonds = que.get()
		pos_list = []

		for newy in range(nwly-factor, nwly+factor+1):
			for newx in range(nwlx-factor, nwlx+factor+1):
				pos_list.append((newx,newy))
				if not (newx, newy) in diamonds:
					#print "making squares..."
					ds = DiamondSquare((newx,newy), (offset+1, offset+1), h_range)
					ds.diamond_square_tile(diamonds)
					diamonds[(newx,newy)] = ds
					ds.save(PATH+str(newx)+"_"+str(newy)+".bmp")
		
		resp_que.put(pos_list, False)
		resp_que.put(diamonds, False)

		#creat new textures
		new_dic = {}
		copy_list = que.get()
		offset = que.get()
		convert = que.get()
		text_holder = TextureHolder()

		print "process running..."
		for location in pos_list:
			if not location in copy_list:
				#print "created someting"
				x,y = location
		
			        load = LoadTerrain(PATH+str(x)+"_"+str(y)+".bmp", convert, text_holder)
			        heights = load.load()
			
			        if init:
					tex_file_name, face_norms, vert_norms = load.init_createRenderList(heights,str(x)+"_"+str(y))
			        else:
					tex_file_name, face_norms, vert_norms = load.createRenderList(heights,str(x)+"_"+str(y))
			
				big_tup = (tex_file_name, face_norms, vert_norms, heights, x*offset, -y*offset, str(x)+"_"+str(y), pos_list.index(location))
              			new_dic[location] = big_tup

	        print "have new dic"
		resp_que.put(new_dic, False)
		print "enqued"
		#que.close()

	def create_lists(self, copy_list, new_loc):
	#Used to create the call lists		
		
		to_q= Queue()
		resp_q = Queue()

		p = Process(target=self.render_thing, args=(to_q,resp_q,self.initalize,new_loc,self.OFFSET, self.FACTOR))
		p.start()
		
		to_q.put(self.diamonds, False)
		to_q.put(copy_list, False)
		to_q.put(self.OFFSET, False)
		to_q.put(self.rw.convert, False)
		
		print "process....."
		print "get pos_list"
		self.pos_list = resp_q.get()
		self.diamonds = resp_q.get()
		print self.pos_list
		new_dic = resp_q.get()
		dic = self.combine(self.pos_list, new_dic, self.trans.location_var)
		self.trans.location_var = dic
		
		p.join()
		
		print "updating...."
		self.rw.need_lists = True
		self.initalize = False

	def combine(self, pos_list, new_dic, old_dic):
		temp = {}
		for location in pos_list:
			if location in old_dic:
				temp[location] = old_dic[location]

		d = dict(temp.items() + new_dic.items())
		return d
		

if __name__ == "__main__":
	w = World()
