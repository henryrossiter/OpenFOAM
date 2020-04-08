import argparse 
import math
from generatemesh import polar_to_cartesian
import numpy as np
from matplotlib import pyplot as plt

# command line argument for sample data
parser = argparse.ArgumentParser()
parser.add_argument('data',help='path to the sample data')
args = parser.parse_args()

sample_length = 2.0

# ==============================================================================
# retrieve velocity and position for sampled .xy file
# ==============================================================================
def process_vel_xy(path):
	v = []
	inFile = open(path,'r')
	for line in inFile:
		vals = line.strip().split()
		v.append([float(vals[0]),float(vals[1]),float(vals[2])])
	return v

def get_mag(vel):
	return math.sqrt(sum(i**2 for i in vel))
def dot(a,b):
	tot = 0
	for i in range(len(a)):
		tot+= a[i]*b[i]
	return tot

def main():
	v = process_vel_xy(args.data)
	if 'sampleLine1' in args.data:
		x,y,z = polar_to_cartesian(math.pi/4,0.5,0.5)	
		title = 'Theta = pi/4'
	elif 'sampleLine2' in args.data:
		x,y,z = polar_to_cartesian(math.pi/2,0.5,0.5)	
		title = 'Theta = pi/2'	
	else:
		x,y,z = polar_to_cartesian(3*math.pi/4,0.5,0.5)	
		title = 'Theta = 3*pi/4'
	mag = math.sqrt(x**2+y**2+z**2)
	r = [x/mag,y/mag,z/mag]
	d = np.linspace(0,sample_length,len(v))
	v_r = []
	v_theta = []
	for vel in v:
		v_mag = get_mag(vel)
		v_r_val = dot(vel,r)
		v_r.append(v_r_val)
		v_theta.append(v_mag-v_r_val)
	plt.plot(d,v_r,label='radial velocity')
	plt.plot(d,v_theta,label='tangential velocity')
	plt.title(title)
	plt.xlabel('distance from the wall')
	plt.ylabel('velocity')
	plt.show()

main()