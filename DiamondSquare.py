import random
import Image
import math
from Erode import ErodeLandscape

ROUGHNESS = .99
HEIGHT_RANGE = 255

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

class DiamondSquare:

    def __init__(self, location, size, h_range):
        self.hrange1, self.hrange2 = h_range
        self.mu = float(self.hrange2 + self.hrange1)/2
        #print self.mu
        self.sigma = float(self.hrange2 - self.mu) / 2
        #print self.sigma
	self.x, self.y = location
	self.width = size[0]
	self.height = size[1]
   	self.heights = []
        for r in range(self.height):
            self.heights.append([0] * self.width)

        self.current_roughness = ROUGHNESS
        self.erode = ErodeLandscape()
    
    def __getitem__(self, xy):
        x, y = xy
        return self.heights[x][y]

    def __setitem__(self, xy, value):
        x, y = xy
        self.heights[x][y] = value

    def __len__(self):
        return self.width

    def get_random_height(self):
        '''Get a completely random height'''
        perc = random.random()
        return int(max(min(random.gauss(self.mu, self.sigma), 255), 0))
        #return random.randrange(self.hrange1, self.hrange2)

    def get_noise(self, roughness):
        '''Get a random number between -roughness and roughness
        and use that to scale based on the HEIGHT_RANGE'''
        return random.gauss(0, roughness*float(self.hrange2)/2)
        
        #return random.uniform(-roughness, roughness) * self.hrange2

    def average(self, *args):
        '''Average a bunch of numbers.'''
        total = 0.0
        for value in args:
            total += value
        return total / len(args)
       

    def set_new_heights(self, start_row, start_col, square_size, roughness):
        '''Calculate new middle and edge-middle heights.
        Each new height is offset by a random amount of noise.'''
        midpoint_y = start_row + (square_size / 2)
        midpoint_x = start_col + (square_size / 2)

        end_row = start_row + square_size
        end_col = start_col + square_size

        a = self[(start_col, start_row)]
        b = self[(end_col, start_row)]
        c = self[(start_col, end_row)]
        d = self[(end_col, end_row)]

        self[(midpoint_x, midpoint_y)] = self.average(a, b, c, d) + self.get_noise(roughness)

        e = self[(midpoint_x, midpoint_y)]


        if self[(midpoint_x, start_row)] == 0:
            self[(midpoint_x, start_row)] = self.average(a, b, e) + self.get_noise(roughness)
        if self[(midpoint_x, end_row)] == 0:
            self[(midpoint_x, end_row)] = self.average(c, d, e) + self.get_noise(roughness)
        if self[(start_col, midpoint_y)] == 0:
            self[(start_col, midpoint_y)] = self.average(a, c, e) + self.get_noise(roughness)
        if self[(end_col, midpoint_y)] == 0:
            self[(end_col, midpoint_y)] = self.average(b, d, e) + self.get_noise(roughness)

     
    def iterate(self):
        '''Generate new heights.
        For different size squares, calculate new middle heights and new edge middle heights.'''
        square_size = self.width-1
        roughness = ROUGHNESS

        while square_size > 1:
            # Reduce roughness as square size decreases
            roughness *= math.pow(2, -ROUGHNESS)

            for start_row in range(0, self.height-square_size+1, square_size):
                for start_col in range(0, self.width-square_size+1, square_size):
                    self.set_new_heights(start_row, start_col, square_size, roughness)

            square_size /= 2



    def diamond_square(self):
        '''Start the diamond-square algorithm.'''
        # Set four corners with initial values
        self[0,0] = self.get_random_height()
        self[0,-1] = self.get_random_height()
        self[-1,0] = self.get_random_height()
        self[-1,-1] = self.get_random_height()
        self.iterate()
        #self.erode.smooth_edges(self, [True,True,True,True])


    def diamond_square_tile(self, neighbors):
        '''Create a new HeightMap that lines up with this Heightmap on a particular side.
        This is used for tiling the Heightmaps in a relatively seamless way.'''
	        
	corners = [(0,0), (-1,0), (-1,-1), (0,-1)]#counter-clockwise from top-left
        edges = [True,True,True,True]

	if len(neighbors) == 0:
		self.diamond_square()
                
	else:
		#if has neighbor to left
	    	if (self.x-1, self.y) in neighbors:
		  # Left side of new Heightmap is seeded
			#print "has left"
			for y in range(self.height):
			    #print neighbors[(self.x-1, self.y)][-1, y]
			    self[0, y] = neighbors[(self.x-1, self.y)][-1, y]
			
			if (0,0) in corners:	
				corners.remove((0,0))
			if (0,-1) in corners:
				corners.remove((0,-1))
                        edges[3] == False
		    
			#if has neighbor to right
	    	if (self.x+1, self.y) in neighbors:
		        # Right side of new Heightmap is seeded
			for y in range(self.height):
		            self[-1, y] = neighbors[(self.x+1, self.y)][0, y]
			
			if (-1,0) in corners:	
				corners.remove((-1,0))
			if (-1,-1) in corners:
				corners.remove((-1,-1))	
			edges[1] = False

			#if has neighbor down
		if (self.x, self.y+1) in neighbors:
		        # Bottom of new Heightmap is seeded
		        for x in range(self.width):
		            self[x, -1] = neighbors[(self.x, self.y+1)][x, 0]
			
			if (0,-1) in corners:	
				corners.remove((0,-1))
			if (-1,-1) in corners:
				corners.remove((-1,-1))	
                        edges[2] = False

			#if has neighbor up		       
		if (self.x, self.y-1) in neighbors:
		        # Top of new Heightmap is seeded
		        for x in range(self.width):
		            self[x, 0] = neighbors[(self.x, self.y-1)][x, -1]
			
			if (0,0) in corners:	
				corners.remove((0,0))
			if (-1,0) in corners:
				corners.remove((-1,0))	
                        edges[0] = False

		for corner in corners:   
			self[corner[0], corner[1]] = self.get_random_height()

		self.iterate()
                #self.erode.smooth_edges(self, edges)
        self.erode.run(2, self, edges)

    def save(self, filename):
        '''Save the HeightMap into an image file (.bmp)'''
        im = Image.new("L", (self.width, self.height))
	pixels = im.load()
        for y in range(self.height):
            for x in range(self.width):
                im.putpixel((x,y),self[(x, y)])#im.putpixel((x, y), self[(x,y)])
        im.save(filename)
