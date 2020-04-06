import argparse, os
from scipy.fft import fft
import matplotlib.pyplot as plt

# command line argument for probe data
parser = argparse.ArgumentParser()
parser.add_argument('data',help='path to the probe data')
args = parser.parse_args()

# open the file and read contents
data_file = open(args.data_file,'r')

# Fourier transform on the data
y = fft(x)

# plot the transform and find frequency of peak
