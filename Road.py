

class Road():
    
    def __init__(self):
        #dictionary to hold roads, possibilty of multiple roads on a map
        self.road_dic = {} #dic {location:[((beginx, beginy),(endx,endy)),...], ...}
        
    #create a road from neighbors tiles
    def create_yroad(self, heights, location, size):
        #inital run for individal tiles, y direction road
        #test phase

        beginx = 15  
        endx = 15
        size = 3
        route = self.find_route(beginx, endx, 0, len(heights[0]), "y", heights)

        for x, y in route:
            self.road_slice(x, y, size, heights, "y")

        return heights

    #pull a road slice out 
    def road_slice(self, x, y, size, heights, axis):
        if axis == "y":
            height = heights[x][y] * .75
            for indx in range(x-size, x+size):
                #print indx, y
                heights[indx][y] = height
                if heights[indx][y] < 1.0:
                    heights[indx][y] = 1.0

    #find a route betweent two points
    def find_route(self, bx, ex, by, ey, axis, heights):
        #within 5
        sizel = 5
        left = False
        right = False
        points = []
        if axis == "y":
            currx = bx
            for y in range(ey):
                if currx - ex > 0: #end x is to the left of currx
                    currx -= 1
                elif currx - ex < 0:#end x is to the right of currx
                    currx += 1
                
                points.append((currx,y))
                    
        return points
