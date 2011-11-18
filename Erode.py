import Image

class ErodeLandscape:
    TALUS_N = 16
    def __init__(self, image):
        self.image = image
        self.pix = image.load()
        self.talus = self.TALUS_N/image.size[0]

    def run(self, iterations):
        for i in range(iterations):
            self.erode()

    def erode(self):
        for x in range(1, self.image.size[0]-1):
            for y in range(1, self.image.size[1]-1):
                d_max = 0
                d_max_spot = 0
                h_center = self.pix[x,y]
                neighbors = self.get_neighbors(x, y)
                for neighbor in neighbors:
                    d_i = h_center - pix[neighbor[0], neightbor[1]]
                    if d_i > d_max:
                        d_max = d_i
                        d_max_spot = neighbor
                if 0 < d_max and d_max >= self.talus:
                    dh = d_max/2
                    pix[x, y] = pix[x, y] - dh
                    pix[d_max_spot[0], d_max_spot[1]] = pix[d_max_spot[0], d_max_spot[1]] + dh

    def get_neighbors(self, x, y):
        x0 = max(x-1, 1)
        x1 = min(x+1, self.image.size[0]-2)
        y0 = max(y-1, 1)
        y1 = min(y+1, self.image.size[1]-2)

        return [(x0,y0), (x1,y0), (x0,y1), (x1,y1)]
