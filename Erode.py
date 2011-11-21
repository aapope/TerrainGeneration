import Image

class ErodeLandscape:
    TALUS_N = 16

    def run(self, iterations, im):
        self.talus = float(self.TALUS_N)/len(im)
        self.pix = im
        self.new_pix = im
        for i in range(iterations):
            self.erode()
        return self.new_pix



    #Need to keep the edge the same, then the next few lines similar. Maybe constrain the slope somehow?
    def erode(self):
        for x in range(0, len(self.pix)):
            for y in range(0, len(self.pix)):
                d_max = 0
                d_max_spot = 0
                h_center = self.pix[x,y]
                neighbors = self.get_neighbors(x, y)
                for neighbor in neighbors:
                    d_i = h_center - self.pix[neighbor[0], neighbor[1]]
                    if d_i > d_max:
                        d_max = d_i
                        d_max_spot = neighbor
                if 0 < d_max and d_max >= self.talus:
                    dh = d_max/2
                    if not self.is_edge(x,y):
                        self.new_pix[x, y] = self.pix[x, y] - dh
                    if not self.is_edge(d_max_spot[0], d_max_spot[1]):
                        self.new_pix[d_max_spot[0], d_max_spot[1]] = self.pix[d_max_spot[0], d_max_spot[1]] + dh

    def get_neighbors(self, x, y):
        x0 = x-1
        x1 = x
        x2 = x+1
        y0 = y-1
        y1 = y
        y2 = y+1
        neighbors = []
        poss_neighbors = [(x0,y0), (x0,y1), (x0,y2), (x1,y0), (x1,y2), (x2,y0), (x2,y1), (x2,y2)]
        for n in poss_neighbors:
            try:
                g = self.pix[n[0], n[1]]
                neighbors.append(n)
            except:
                pass
        return neighbors

    def is_edge(self, x, y):
        if x==0 or y==0 or x==len(self.pix)-1 or y==len(self.pix)-1:
            return False
        else:
            return False


    def smooth_edges(self, pix, corners):
        self.talus = float(self.TALUS_N)/len(pix)
        if corners[0]:
            self.smooth_edge((False,True),0, pix)
        if corners[1]:
            self.smooth_edge((True,False),len(pix)-1, pix)
        if corners[3]:
            self.smooth_edge((False,True),len(pix)-1, pix)
        if corners[2]:
            self.smooth_edge((True,False),0, pix)

    def smooth_edge(self, xy, static, pix):
        if xy[0]:
            x = static
            for y in range(len(pix)):
                self.do_once(x, y, pix, 'y')
        else:
            y = static
            for x in range(len(pix)):
                self.do_once(x, y, pix, 'x')

    def do_once(self, x, y, pix, axis):
        d_max = 0
        d_max_spot = 0
        h_center = pix[x,y]

        if axis == 'x':
            neighbors = ((max(x-1, 0), y), (min(x+1,len(pix)-1), y))
        else:
            neighbors = ((x, max(y-1,0)), (x,min(y+1,len(pix)-1)))

        for neighbor in neighbors:
            d_i = h_center - pix[neighbor[0], neighbor[1]]
            if d_i > d_max:
                d_max = d_i
                d_max_spot = neighbor
            if 0 < d_max and d_max >= self.talus:
                dh = d_max/2
                pix[x, y] = pix[x, y] - dh
                pix[d_max_spot[0], d_max_spot[1]] = pix[d_max_spot[0], d_max_spot[1]] + dh

    def save(self):
        self.new_im.save('new.bmp')

if __name__ == '__main__':
    im = Image.open('data/heightmaps/maps/0_0.bmp')
    ERODE = ErodeLandscape()
    ERODE.run(50, im.load())
