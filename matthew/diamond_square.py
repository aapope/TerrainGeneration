
import random
import Image
import math

ROUGHNESS = .9
HEIGHT_RANGE = 255

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

class HeightMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.heights = []
        for r in range(height):
            self.heights.append([0] * width)

        self.current_roughness = ROUGHNESS
    
    def __getitem__(self, xy):
        x, y = xy
        return self.heights[y][x]

    def __setitem__(self, xy, value):
        x, y = xy
        self.heights[y][x] = value

    def get_random_height(self):
        '''Get a completely random height'''
        return random.randrange(0, HEIGHT_RANGE)

    def get_noise(self, roughness):
        '''Get a random number between -roughness and roughness
        and use that to scale based on the HEIGHT_RANGE'''
        return random.uniform(-roughness, roughness) * HEIGHT_RANGE

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


    def diamond_square_tile(self, direction=RIGHT):
        '''Create a new HeightMap that lines up with this Heightmap on a particular side.
        This is used for tiling the Heightmaps in a relatively seamless way.'''
        
        # New tile is the same size as the existing Heightmap
        new_hm = HeightMap(self.width, self.height)

        # Tile to the right
        if direction == RIGHT:
            # Left side of new Heightmap is seeded
            for y in range(self.height):
                new_hm[0, y] = self[-1, y]

            new_hm[-1,0] = self.get_random_height()
            new_hm[-1,-1] = self.get_random_height()

        # Tile to the left
        elif direction == LEFT:
            # Right side of new Heightmap is seeded
            for y in range(self.height):
                new_hm[-1, y] = self[0, y]

            new_hm[0,0] = self.get_random_height()
            new_hm[0,-1] = self.get_random_height()

        # Tile up
        elif direction == UP:
            # Bottom of new Heightmap is seeded
            for x in range(self.width):
                new_hm[x, -1] = self[x, 0]

            new_hm[0,0] = self.get_random_height()
            new_hm[-1,0] = self.get_random_height()

        # Tile down
        elif direction == DOWN:
            # Top of new Heightmap is seeded
            for x in range(self.width):
                new_hm[x, 0] = self[x, -1]

            new_hm[0,-1] = self.get_random_height()
            new_hm[-1,-1] = self.get_random_height()

        new_hm.iterate()

        return new_hm


    def save(self, filename):
        '''Save the HeightMap into an image file (.bmp)'''
        im = Image.new("L", (self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                im.putpixel((x, y), self[(x,y)])
        im.save(filename)


def main(size, filename):
    '''Creates a new HeightMap, runs diamond-square to generation heights, and saves the file.
    size should be one more than a power of two: 2^n + 1.
    Square heightmaps are generated.'''
    hm = HeightMap(size, size)
    hm.diamond_square()

    # Create 4 new Heightmaps
    hm_right = hm.diamond_square_tile(RIGHT)
    hm_left = hm.diamond_square_tile(LEFT)
    hm_up = hm.diamond_square_tile(UP)
    hm_down = hm.diamond_square_tile(DOWN)

    # Save all Heightmaps to .bmp files
    hm.save(filename)
    hm_right.save("RIGHT" + filename)
    hm_left.save("LEFT" + filename)
    hm_up.save("UP" + filename)
    hm_down.save("DOWN" + filename)


if __name__=="__main__":
    import sys
    # main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
    main(129, sys.argv[1])


