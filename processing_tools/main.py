import argparse
from post_process_functions import process_vel_xy

parser = argparse.ArgumentParser()
parser.add_argument('path',help='path to sampled .xy data file')
args = parser.parse_args()

# get the values for velocity and position
x,y,z,u,v,w = process_vel_xy(args.path)