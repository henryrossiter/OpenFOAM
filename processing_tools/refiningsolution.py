from visualizations import *
from post_process_functions import process_vel_xy
import numpy as np
from scipy.stats import linregress

gridsizes = [20,40,80,160]
timesteps = [0.005, .0025, .00125, .000625]
clocktimes = [1.704, 5.217, 21.01, 224.815]
threedim = False

if threedim:
    ##FOR CASE OF 3D PLOT OVER ALL TIMESTEPS
    for grid, step in zip(gridsizes, timesteps):
        outer_path = ("/Users/danielfonseka/Documents/COE347/Computational-Fluid-Dynamics/cavity/postProcessing/"
                "postprocess_" + str(grid) + "x" + str(grid) + "_x=0.5" )

        times = np.around(np.arange(0,0.5, (2*step)),5)

        x,y,z,u,v,w,t = [],[],[],[],[],[], []
        for time in times:
            
            time = np.format_float_positional(time, unique=True)

            if time == "0.":
                time = 0
            inner_path = "/" + str(time) + "/center_cavity_U.xy"
            
            x_0,y_0,z_0,u_0,v_0,w_0 = process_vel_xy(outer_path + inner_path)
            t_0 = np.full(shape=len(x_0), fill_value=time)

            x.append(x_0)
            y.append(y_0) 
            z.append(z_0)
            u.append(u_0)
            v.append(v_0)
            w.append(w_0)
            t.append(t_0.tolist())
        
        flat = lambda l: [float(item) for sublist in l for item in sublist]


        velocity_comps_2D_times(flat(x),flat(y),flat(u),flat(v),flat(t),grid)
else:
    ##FOR CASE OF 2D PLOT OF ONLY ONE TIMESTEP
    for grid, step in zip(gridsizes, timesteps):
        path = ("/Users/danielfonseka/Documents/COE347/Computational-Fluid-Dynamics/cavity/postProcessing/"
            "postprocess_" + str(grid) + "x" + str(grid) + "_x=0.5" "/" + str(0.5) + "/center_cavity_U.xy")
        
        x,y,z,u,v,w = process_vel_xy(path)

        velocity_comps_2D(x,y,u,v,grid)

clocktime_vs_gridsize(gridsizes, clocktimes)

regression = linregress(np.log(gridsizes), np.log(clocktimes))
alpha = regression[0]

print("The alpha value is ", alpha)
