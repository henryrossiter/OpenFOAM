# Functions useful for post processing 

# ==============================================================================
# retrieve velocity and position for sampled .xy file
# ==============================================================================
def process_vel_xy(path):
	u,v,w,x,y,z = [],[],[],[],[],[]
	inFile = open(path,'r')
	for line in inFile:
		vals = line.strip().split()
		x.append(float(vals[0]))
		y.append(float(vals[1]))
		z.append(float(vals[2]))
		u.append(float(vals[3]))
		v.append(float(vals[4]))
		w.append(float(vals[5]))
	return x,y,z,u,v,w
