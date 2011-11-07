import numpy

def calc_normal(v0, v1):
    normal = numpy.cross(v0,v1)
    return normalize(normal)
    
def normalize(vector):
    norm = numpy.linalg.norm(vector)
    return (vector[0]/norm,vector[1]/norm,vector[2]/norm)

def get_vector(v0, v1):
    x = v1[0] - v0[0]
    y = v1[1] - v0[1]
    z = v1[2] - v0[2]
    return numpy.array([x,y,z])

def calc_face_normals(heights, x_scale, z_scale):
    '''dict of face normals with vertex : array of face normals it's a part of'''
    face_normals = {}
    for z in range(0, len(heights)-1):
        for x in range(0, len(heights[z])-1):
            p0 = ((x+1)*x_scale, heights[z][x+1], -z*z_scale)
            p1 = (x*x_scale, heights[z+1][x], -(z+1)*z_scale)
            p2 = (x*x_scale, heights[z][x], -z*z_scale)
            p3 = ((x+1)*x_scale, heights[z+1][x+1], -(z+1)*z_scale)
            
            v0 = get_vector(p0, p1)
            v1 = get_vector(p0, p2)
            v2 = get_vector(p0, p3)
            
            f0 = calc_normal(v0, v1)
            f1 = calc_normal(v2, v0)
            

            if not p0 in face_normals:
                face_normals[p0] = [f0, f1]
            else:
                face_normals[p0].append(f0)
                face_normals[p0].append(f1)

            if not p1 in face_normals:
                face_normals[p1] = [f0, f1]
            else:
                face_normals[p1].append(f0)
                face_normals[p1].append(f1)

            if not p2 in face_normals:
                face_normals[p2] = [f0]
            else:
                face_normals[p0].append(f0)

            if not p3 in face_normals:
                face_normals[p3] = [f1]
            else:
                face_normals[p3].append(f1)
    return face_normals

def calc_vert_normals(point, face_normals):
    avg = [0,0,0]
    for face in face_normals[point]:
        avg[0] += face[0]
        avg[1] += face[1]
        avg[2] += face[2]

    leng = len(face_normals[point])
    avg[0] /= leng
    avg[1] /= leng
    avg[2] /= leng

    return (avg[0],avg[1],avg[2])
