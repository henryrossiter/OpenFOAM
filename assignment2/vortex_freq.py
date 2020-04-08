import argparse, os
from scipy.fftpack import fft, fftfreq, fftshift
import matplotlib.pyplot as plt
import math

# command line argument for probe data
parser = argparse.ArgumentParser()
parser.add_argument('data',help='path to the probe data')
args = parser.parse_args()

#==================================================
# reads probe file and returns time and velocity
#==================================================
def read_file(data_file):
	t = []
	u = []
	count = 0
	while '#' in data_file.readline():
		count+=1
		u.append([])
		pass
	u.pop()
	u.pop()	
	for line in data_file:
		time = line.strip().split()[0]
		vels = line.strip().split('(')[1:]
		t.append(float(time.strip()))
		for i,vel in enumerate(vels):
			mag_v = math.sqrt(sum(float(i)**2 for i in vel.strip().strip(')').split()))
			u[i].append(mag_v)
	return t,u


def main():
	# open the file and read contents
	if not os.path.exists(args.data):
		path = os.getcwd() + os.path.sep + args.data
	else:
		path = args.data
	data_file = open(path,'r')
	time, vel = read_file(data_file)
	data_file.close()
	for i,velocity in enumerate(vel):
		# plot velocity vs. time
		plt.figure()
		plt.plot(time,velocity)
		plt.xlabel('time')
		plt.ylabel('velocity')
		plt.title('Probe '+str(i))
		plt.show()

		# Fourier transform on the data
		freq = fftfreq(len(time))
		u = fft(velocity)

		# plot the transform and find frequency of peak
		plt.figure()
		plt.plot(freq,u.real,freq,u.imag)
		plt.xlabel('frequency')
		plt.ylabel('power spectral density')
		plt.title('Probe '+str(i))
		plt.show()
main()