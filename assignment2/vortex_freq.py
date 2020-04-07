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
	while '#' in data_file.readline():
		pass
	t = []
	u = []
	for line in data_file:
		time, vel = line.strip().split('(')
		t.append(float(time.strip()))
		mag_v = math.sqrt(sum(float(i)**2 for i in vel.strip(')').split()))
		u.append(mag_v)
	return t,u


def main():
	# open the file and read contents
	if not os.path.exists(args.data):
		path = os.getcwd() + os.path.sep + args.data
	else:
		path = args.data
	data_file = open(path,'r')
	time, velocity = read_file(data_file)
	data_file.close()
	# plot velocity vs. time
	plt.figure()
	plt.plot(time,velocity)
	plt.xlabel('time')
	plt.ylabel('velocity')
	plt.show()

	# Fourier transform on the data
	freq = fftshift(fftfreq(len(time)))
	u = fftshift(fft(velocity))

	# plot the transform and find frequency of peak
	plt.figure()
	plt.plot(freq,u.real,freq,u.imag)
	plt.xlabel('frequency')
	plt.ylabel('power spectral density')
	plt.show()
main()