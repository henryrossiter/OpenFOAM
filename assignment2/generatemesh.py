import numpy as np
from matplotlib import pyplot as plt
from itertools import count
import os

class Block:

    _ids = count(0)
    _arcnum = count(0)

    def __init__(self,pointdict,l1,l2,l3,l4,l5,l6,l7,l8,boxsize):
        self.points = pointdict
        self.boxsize = boxsize
        self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7, self.l8 = l1,l2,l3,l4,l5,l6,l7,l8
        self.x1,self.x2,self.x3,self.x4 = self.points[l1], self.points[l2], self.points[l3], self.points[l4]
        self.x5,self.x6,self.x7,self.x8 = self.points[l5], self.points[l6], self.points[l7], self.points[l8]
        self.blocknum = next(self._ids)
        self.local2global = {1:l1, 2: l2,3:l3, 4: l4, 5:l5, 6: l6,7:l7, 8: l8}
        
        self.facedict = {"top": [], "bottom":[], "inlet":[], "outlet":[], "cylinder": [], "useless": []}
        self.arcdict = {}

        self.create_faces()

    def set_grids(self, x, y, z):
        self.xsize = x
        self.ysize = y
        self.zsize = z
    
    def set_arcs(self, p1, p2):
        theta1, r1, z1 = cartesian_to_polar(self.points[p1][0], self.points[p1][1], self.points[p1][2])
        theta2, r2, z2 = cartesian_to_polar(self.points[p2][0], self.points[p2][1], self.points[p2][2])
        if np.isclose(r1,r2,1e-3,1e-3):
            newtheta = np.mean(np.asarray([theta1, theta2]))
            x,y,z = polar_to_cartesian(newtheta,r1,z1) #assumes arcs in same z plane

            self.arccount = next(self._arcnum)
            self.arcdict[self.arccount] = (p1, p2, (x,y,z))

        else:
            print("Radii don't match for some reason")
            print(p1)
            print(p2)
            print(self.points[p1][0], self.points[p1][1], self.points[p1][2])
            print(self.points[p2][0], self.points[p2][1], self.points[p2][2])
            print("Radius 1", r1)
            print("Radius 2", r2)
            raise ValueError

    def create_faces(self):
        f1 = (self.l1, self.l5, self.l8, self.l4)
        f2 = (self.l2, self.l6, self.l7, self.l3)
        f3 = (self.l1, self.l2, self.l6, self.l5)
        f4 = (self.l4, self.l3, self.l7, self.l8)

        for face in [f1,f2,f3,f4]:
            label = self.classify_face(face)
            self.facedict[label].append(face)


    def classify_face(self,face):

        #counter  = {"top": 0, "bottom":0, "inlet":0, "outlet":0, "cylinder": 0, "useless": 0}

        if self.points[face[0]][0] == self.points[face[1]][0] == self.points[face[2]][0] == self.points[face[3]][0] ==self.boxsize/2:
            label = "top"
        elif self.points[face[0]][0] == self.points[face[1]][0] == self.points[face[2]][0] == self.points[face[3]][0] == - self.boxsize/2:
            label = "bottom"
        elif self.points[face[0]][1] == self.points[face[1]][1] == self.points[face[2]][1] == self.points[face[3]][1] == self.boxsize/2:
            label = "outlet"
        elif self.points[face[0]][1] == self.points[face[1]][1] == self.points[face[2]][1] == self.points[face[3]][1] == - self.boxsize/2:
            label = "inlet"
        elif (c2pT(self.points[face[0]])[1]  < 0.51 and c2pT(self.points[face[1]])[1] < 0.51 and c2pT(self.points[face[2]])[1] < 0.51 and c2pT(self.points[face[0]])[1] <0.51):
            print(c2pT(self.points[face[0]])[1] , c2pT(self.points[face[1]])[1] , c2pT(self.points[face[2]])[1] , c2pT(self.points[face[0]])[1])
            label = "cylinder"
        else:
            label = "useless"
        return label


""" 

        for vertex in face:
            
            
            r = cartesian_to_polar(self.points[vertex][0],self.points[vertex][1],self.points[vertex][2])[1]
            label = "useless"
            if self.points[vertex][0] == self.boxsize / 2:
                counter["outlet"] += 1
            elif self.points[vertex][0] == - self.boxsize / 2:
                counter["inlet"] += 1
            elif self.points[vertex][1] == self.boxsize / 2:
                counter["top"] += 1
            elif self.points[vertex][1] == - self.boxsize / 2:
                counter["bottom"] += 1
            elif r <  0.6:
                counter["cylinder"] += 1

        val=list(counter.values())
        key=list(counter.keys())
        print(key[val.index(max(val))])
        return key[val.index(max(val))] """


def polar_to_cartesian(theta, r, z):
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = z
    return np.around(x,3), np.around(y,3), z

def cartesian_to_polar(x,y,z):
    r = np.sqrt(np.square(x) + np.square(y))

    theta = np.arctan(y/x)
    x = z
    return np.around((theta,3)), np.around(r,3), z

def c2pT(pointtuple):
    x = pointtuple[0]
    y = pointtuple[1]
    z = pointtuple[2]

    return cartesian_to_polar(x,y,z)



def pointlist_to_dict(pointlist, pointdict):
    if not pointdict:
        for i in range(len(pointlist)):
            pointdict[i] = pointlist[i]
    else:
        j = len(pointdict)
        for i in range(len(pointlist)):
            pointdict[i + j] = pointlist[i]

    return pointdict

def add_z_layer(pointdict, coord):
    copy = pointdict.copy()
    length = len(pointdict)
    for key, value in copy.items():
        if key == length:
            break
        newkey = key + length
        pointdict[newkey] = (value[0], value[1], coord)

    return pointdict


def main():

    diameter = 1 #meter
    outerdiameter = 3 
    radius = diameter / 2
    outerradius = 3 / 2
    boxsize = 10 #both height and width (same)

    circlepoints = 8 # better if even number
    thetas = np.linspace(0,2*np.pi, circlepoints, endpoint = False)
    radii = lambda fac : np.full(thetas.shape, fac)
    zees = np.full(thetas.shape, 0) # z coordinate for first layer

    innercircle = [(x,y,z) for (x,y,z) in zip(*polar_to_cartesian(thetas, radii(radius), zees))]
    outercircle = [(x,y,z) for (x,y,z) in zip(*polar_to_cartesian(thetas, radii(outerradius), zees))]

    pioverfour, _, _  = np.abs(polar_to_cartesian(np.pi/4, outerradius, 0))

    #TODO: Fix top and right so that the correct corner boxes are created for any even number of circlepoints
    top = list(dict.fromkeys([(x,boxsize / 2,z) for (x,y,z) in outercircle if np.abs(x) <= pioverfour+0.001]))
    bottom  = [(x,-y,z) for (x,y,z) in top]
    right = list(dict.fromkeys([(boxsize / 2, y, z) for (x,y,z) in outercircle if np.abs(y) <= pioverfour]))
    left = [(-x,y,z) for (x,y,z) in right]
    corners = [(-boxsize/2, -boxsize/2,0), (boxsize/2, -boxsize/2,0), (-boxsize/2, boxsize/2,0), (boxsize/2, boxsize/2,0)]

    def rightorder(inputpoints):
        points = sorted(inputpoints)
        negatives = []
        positives = []
        for i in range(len(points)):
            if points[i][1] < 0 :
                negatives.append(points[i])
            else:
                positives.append(points[i])

        return positives, negatives

    #sort lists into clockwise order
    topright, bottomright = rightorder(right)
    left = sorted(left, reverse = True)
    bottom = sorted(bottom)


    points = {} # dictionary that will contain the number and corresponding coordiantes of each point

    for pointlist in [innercircle, outercircle, topright,[corners[3]], top,[corners[2]], left,[corners[0]], bottom, [corners[1]], bottomright]:
        points = pointlist_to_dict(pointlist, points)    

    k = len(points)

    #create second z layer at z = 1 (copy over x and y) and add to points list
    points = add_z_layer(points,1)

    n = circlepoints
    blocks = {}

    #this is the block creation logic, unfortunately right now half of it is hard coded and will only work with n = 8. 
    #(working on it)
    for i in points.keys():
        if i < n-1:
            blocks[i] = Block(points, i, i+n, i+n+1, i+1, i+k, i+k+n, i+k+n+1, i+k+1, boxsize)
            blocks[i].set_arcs(i, i+1)
            blocks[i].set_arcs(i+k, i+1+k)
            blocks[i].set_arcs(i+n, i+n+1)
            blocks[i].set_arcs(i+k+n, i+1+k+n)
        elif i == n-1:
            blocks[i] = Block(points, i, i+n, n, 0, i+k, i+k+n, n+k, k, boxsize)
            blocks[i].set_arcs(i, 0)
            blocks[i].set_arcs(i+k, k)
            blocks[i].set_arcs(i+n, n)
            blocks[i].set_arcs(i+k+n, n+k)
        
        #TODO: Make this extensible, and not hard coded for circlepoint = 8
        if n != 8:
            "lol not ready for that shit yet"
            raise  ValueError
        blocks[8] = Block(points, 8, 16, 17, 9, 8+k, 16+k, 17+k, 9+k, boxsize)
        blocks[9] = Block(points, 9, 17, 18, 19, 9+k, 17+k, 18+k, 19+k, boxsize)
        blocks[10] = Block(points, 9, 19, 20, 10, 9+k, 19+k, 20+k, 10+k, boxsize)
        blocks[11] = Block(points, 10, 20, 21, 11, 10+k, 20+k, 21+k, 11+k, boxsize)
        blocks[12] = Block(points, 11, 21, 22, 23, 11+k, 21+k, 22+k, 23+k, boxsize)
        blocks[13] = Block(points, 11, 23, 24, 12, 11+k, 23+k, 24+k, 12+k, boxsize)

        blocks[14] = Block(points, 8+4, 16+8, 17+8, 9+4, 8+k+4, 16+k+8, 17+k+8, 9+k+4, boxsize)
        blocks[15] = Block(points, 9+4, 17+8, 18+8, 19+8, 9+k+4, 17+k+8, 18+k+8, 19+k+8, boxsize)
        blocks[16] = Block(points, 9+4, 19+8, 20+8, 10+4, 9+k+4, 19+k+8, 20+k+8, 10+k+4, boxsize)
        blocks[17] = Block(points, 10+4, 20+8, 21+8, 11+4, 10+k+4, 20+k+8, 21+k+8, 11+k+4, boxsize)
        blocks[18] = Block(points, 11+4, 21+8, 22+8, 23+8, 11+k+4, 21+k+8, 22+k+8, 23+k+8, boxsize)
        blocks[19] = Block(points, 15, 31, 16, 8, 15+k, 31+k, 16+k, 8+k, boxsize)
        

    #creates graph as visual aid (uncomment plt.show() to see)
    for i,val in points.items():

        x = val[0]
        y = val[1]
        plt.scatter(x, y, marker='x', color='red')
        if i < k:
            plt.text(x+0.1, y+0.3, str(i), fontsize=7)
        else:
            plt.text(x-0.1, y+0.3, str(i), fontsize=7)
    #plt.show()

    #writes blockmeshdict file
    to_file("blockMeshDict", points, blocks)


def to_file(filename, points, blocks):

    if os.path.exists(filename):
        os.remove(filename)

    f = open(filename, "a")
    f.write("""FoamFile
{
    version  2.0;
    format   ascii; 
    class    dictionary;
    object   blockMeshDict;
}

convertToMeters 1.0;

vertices
( """)

    for number, point in points.items():
        f.write("\t" + str(point).replace(',', '') + "\n")

    f.write("""
);

blocks
(
""")

    for key, block in blocks.items():
        f.write("\thex ("  + str(block.l1).replace(',', '') + " "+str(block.l2).replace(',', '') + " "+str(block.l3).replace(',', '') + " "+str(block.l4).replace(',', '') + 
            " "+str(block.l5).replace(',', '') + " "+str(block.l6).replace(',', '') + " "+str(block.l7).replace(',', '') + " "+str(block.l8).replace(',', '') + 
            ") (10 20 1) simpleGrading (2.0 1.0 1.0) \n")

    f.write(""");

edges
(""")

    for key, block in blocks.items():
        for i, arc in block.arcdict.items():
            f.write("\tarc " + str(arc[0]).replace(',', '')  + " "+ str(arc[1]).replace(',', '') + " " + str(arc[2]).replace(',', '') + "\n")

    f.write("""
);

boundary
(

  inlet
  {
      type patch;
      faces
      (
""")

    for key, block in blocks.items():
        for inlet in block.facedict["inlet"]:
            f.write("\t\t" + str(inlet).replace(',', '') + "\n")


    f.write(""" 
      );
  }

  outlet
  {
      type patch;
      faces
      (
""")

    for key, block in blocks.items():
        for inlet in block.facedict["outlet"]:
            f.write("\t\t" + str(inlet).replace(',', '') + "\n")


    f.write("""
      );
  }

  cylinder
  {
      type wall;
      faces
      (
""")
    for key, block in blocks.items():
        for inlet in block.facedict["cylinder"]:
            f.write("\t\t" + str(inlet).replace(',', '') + "\n")

    f.write("""
      );
  }

  top
  {
      type symmetryPlane;
      faces
      (

""")

    for key, block in blocks.items():
        for inlet in block.facedict["top"]:
            f.write("\t\t" + str(inlet).replace(',', '') + "\n")
    
    f.write("""
      );
  }

  bottom
  {
      type symmetryPlane;
      faces
      (

""")

    for key, block in blocks.items():
        for inlet in block.facedict["bottom"]:
            f.write("\t\t" + str(inlet).replace(',', '') + "\n")


    f.write("""
      );
  }

);
""")


main()
