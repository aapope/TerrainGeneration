import Image

class ErodeLandscape:
    TALUS_N = 16

    def run(self, iterations, im, edges):
        self.talus = float(self.TALUS_N)/len(im)
        self.pix = im
        self.new_pix = im
        self.grab_edges(edges)
        for i in range(iterations):
            self.erode()
        #self.replace_edges()
        return self.new_pix

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
                if 0 < d_max and d_max < self.talus:
                    dh = d_max/16
                    if not self.is_edge(x,y):
                        self.new_pix[x, y] = self.pix[x, y] - dh
                    if not self.is_edge(d_max_spot[0], d_max_spot[1]):
                        self.new_pix[d_max_spot[0], d_max_spot[1]] = self.pix[d_max_spot[0], d_max_spot[1]] + dh

    def grab_edges(self, edges):
        self.edges = [[],[],[],[]]
        if edges[0]:
            for x in range(len(self.pix)):
                self.edges[0].append(self.pix[x, 0])
        if edges[1]:
            for y in range(len(self.pix)):
                self.edges[1].append(self.pix[len(self.pix)-1,y])
        if edges[2]:
            for x in range(len(self.pix)):
                self.edges[2].append(self.pix[x, len(self.pix)-1])
        if edges[3]:
            for y in range(len(self.pix)):
                self.edges[3].append(self.pix[0, y])

    def replace_edges(self):
        es = [False,False,False,False]

        if self.edges[0]:
            es[0] = True
            diffs = []
            for x in range(len(self.pix)):
                diffs.append(self.pix[x, 0] - self.edges[0][x])

            for y in range(len(self.pix)):
                for x in range(len(self.pix)):
                    self.pix[x, 0] -= diffs[x] / (2 ** y)
        if self.edges[1]:
            es[1] = True
            st = 0
            if es[0]:
                st = 1
            diffs = []
            for y in range(len(self.pix)):
                diffs.append(self.pix[len(self.pix)-1, y] - self.edges[1][y])

            for x in range(len(self.pix),0,-1):
                for y in range(1, len(self.pix)):
                    self.pix[len(self.pix)-1, y] -= diffs[y] / (2 ** x)
        if self.edges[2]:
            es[2] = True
            st = 0
            ed = 0
            if es[0]:
                st = 1
            if es[1]:
                ed = 1
            diffs = []
            for x in range(len(self.pix)):
                diffs.append(self.pix[x, len(self.pix)-1] - self.edges[2][x])

            for y in range(len(self.pix),st,-1):
                for x in range(len(self.pix)-ed):
                    self.pix[x, len(self.pix)-1] -= diffs[x] / (2 ** y)
        if self.edges[3]:
            st = 0
            ed = 0
            mv = 0
            if es[0]:
                st = 1
            if es[1]:
                ed = 1
            if es[2]:
                mv = 1
            diffs = []
            for y in range(len(self.pix)):
                diffs.append(self.pix[0, y] - self.edges[3][y])

            for x in range(len(self.pix)-ed):
                for y in range(st, len(self.pix)-mv):
                    self.pix[0, y] -= diffs[y] / (2 ** x)
            
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
            return True
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
