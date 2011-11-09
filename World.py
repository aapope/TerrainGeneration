#class to control graphics and loading of new terrain

XFACTOR = 1
YFACTOR = 25
ZFACTOR = 1

FACTOR = 1
OFFSET = 128
from DiamondSquare import DiamondSquare
from LoadTerrain import LoadTerrain

PATH = ""

class World:

	def __init__(self):
		self.size = 3
		self.curr_x = 0
		self.curr_y = 0
		self.diamonds = {}
		self.index_list = []
		self.pos_list = []
		self.init_world()
		self.create_lists()
		
			
	#Used to create the inital world
	def init_world(self):
		for y in range(-FACTOR, self.size-FACTOR):
			for x in range(-FACTOR, self.size-FACTOR):
				#print "POS:",x,y
				self.pos_list.append((x,y))				
				ds = DiamondSquare((x, y))
				ds.diamond_square_tile(self.diamonds)
				self.diamonds[(x,y)] = ds
				#if (not x == 0 and not y == -1) or (not x == 0 and not y == 0):# or (x != 0 and y != -1):
				ds.save(PATH+str(x)+"_"+str(y)+".bmp")
	
	#Used to update camera location
	def update_loc(self,x,y,z):
		print str(x),",",str(y)+",", str(z)
		x = int(x)
		z = int(z)
		if not self.is_in_tile(x,z,self.curr_x, self.curr_y):		
			newloc = self.get_tile(x,y,z)
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
			if x in range(posx*OFFSET, (posx+1)*(OFFSET)) and z in range((posy)*(OFFSET), (posy-1)*OFFSET, -1):
				return True
			else:
				return False
		else:
			if x in range(posx*OFFSET, (posx+1)*(OFFSET)) and z in range((posy-1)*(OFFSET), (posy)*OFFSET):
				return True
			else:
				return False
		
	#Used to update the world list
	def update_diamonds(self, new_loc):
		x,y = new_loc
		self.pos_list = []
		for newy in range(y-1, y+2):
			for newx in range(x-1, x+2):
				self.pos_list.append((newx,newy))
				if not (newx, newy) in self.diamonds:
					ds = DiamondSquare((newx,newy))
					ds.diamond_square_tile(self.diamonds)
					self.diamonds[(newx,newy)] = ds
					ds.save(PATH+str(newx)+"_"+str(newy)+".bmp")
					print "done updating diamonds"
		
		print self.pos_list
		self.create_lists()
		self.curr_x = x
		self.curr_y = y
		
	#Used to create the call lists
	def create_lists(self):
		
		self.index_list = []
		for location in self.pos_list:
			x,y = location
			print location
			print "/", self.pos_list.index(location)
			load = LoadTerrain(PATH+str(x)+"_"+str(y)+".bmp", (XFACTOR, YFACTOR, ZFACTOR))
			heights = load.load()
			index = load.createRenderList(heights, x*OFFSET, -y*OFFSET,str(x)+"_"+str(y), self.pos_list.index(location))
			
			self.index_list.append(index)
		'''

		load = LoadTerrain(PATH+str(0)+"_"+str(0)+".bmp")
		self.index_list.append(load.createRenderList(load.load(), 0*OFFSET, 0*OFFSET,str(0)+"_"+str(0)))'''
if __name__ == "__main__":
	w = World()
