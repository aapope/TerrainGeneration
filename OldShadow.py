    def shadow_texture(self, pix, heights, size):
        d_pos = self.calc_pixel_positions(pix, heights, size)
        projection = self.rotate_image(d_pos)
        pix_to_shade = self.get_invisible(projection)
        self.apply_shadows(pix, pix_to_shade)

    def calc_pixel_positions(self, pix, heights, size):
        positions = {}

        for y in range(size[0]/16):
            for x in range(size[1]):
                y0 = y
                x0 = x
                z0 = heights[y0/self.SIZE][x0/self.SIZE]

                y1 = min((y0 + 1), size[0]-1)
                x1 = x0
                z1 = heights[y1/self.SIZE][x1/self.SIZE]

                y2 = y0
                x2 = min((x0 + 1), size[1]-1)
                try:
                    z2 = heights[y2/self.SIZE][x2/self.SIZE]
                except:
                    print y2, x2


                A = numpy.linalg.det([[1,y0,z0], [1,y1,z1], [1,y2,z2]]) 
                B = numpy.linalg.det([[x0,1,z0], [x1,1,z1], [x2,1,z2]])
                C = numpy.linalg.det([[x0,y0,1], [x1,y1,1], [x2,y2,1]])
                D = numpy.linalg.det([[x0,y0,z0], [x1,y1,z1], [x2,y2,z2]])
                
                z = (A*x + B*y + D)/(-1*C)
                
                
                positions[(y, x)] = (x, y, z)
        return positions

    def rotate_image(self, positions):
        #Project onto plane y=0, convert to u, v, n coordinates
        projection = {}
        for y, x in positions:
            pos = positions[(y, x)]
            if not (pos[1], pos[2]) in projection:
                projection[(pos[1], pos[2])] = [pos[0]]#proj[(y, z)] = x
            else:
                projection[(pos[1], pos[2])].append(pos[0])
        return projection

    def get_invisible(self, projection):
        to_shade = []
        for y, z in projection:
            to_shade.append((min(projection[(y, z)]), y))#x, y
        return to_shade

    def apply_shadows(self, pix, to_shade):
        for x, y in to_shade:
            pix[y, x] = self.darken(pix[y, x])

    def darken(self, pixel):
        r,g,b = pixel
        
        r = 255#min(r+10,255)
        g = 255#min(g+10,255)
        b = 255#min(b+10,255)

        return (r,g,b)
