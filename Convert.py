
class Convert:

    def __init__(self, height_map, texture, gl, map_size):
        #Tuples for each axis's scale
        self.height_map_scale = height_map
        self.texture_scale = texture
        self.open_gl_scale = gl
        self.sea_level = self.open_gl_scale[1]/float(15)
        self.size = map_size
        #print self.size
        self.gl_x = self.size * self.open_gl_scale[0]
        self.gl_y = self.open_gl_scale[1]
        self.gl_z = self.size * self.open_gl_scale[2]

    def set_dimensions(self, x, z):
        self.heightmap_x = x
        self.heightmap_z = z
        self.texture_x = x * self.texture_scale[0]
        self.texture_z = z * self.texture_scale[2]
        self.gl_x = x * self.open_gl_scale[0]
        self.gl_y = 1 * self.open_gl_scale[1]
        self.gl_z = z * self.open_gl_scale[2]

    def convert(self, from_system, to_system, axis, amt):
        initial_system = self._find_coord_system(from_system)
        final_system = self._find_coord_system(to_system)
        system_axis = self._find_axis(axis)

        converted_amt = amt * final_system[system_axis] / initial_system[system_axis]
        
        return converted_amt
        
    def convert_for_triangle(self, axis, hm_num):
	if axis == 'x':
		return hm_num
	else:
		new_num = hm_num - self.size
		return new_num

    def _find_coord_system(self, name):
        if name == 'h':
            return self.height_map_scale
        elif name == 't':
            return self.texture_scale
        elif name == 'g':
            return self.open_gl_scale
        else:
            return None

    def _find_axis(self, name):
        if name == 'x':
            return 0
        elif name == 'y':
            return 1
        elif name == 'z':
            return 2
        else:
            return None
