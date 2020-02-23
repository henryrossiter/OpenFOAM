from matplotlib import pyplot as plt, rcParams
from mpl_toolkits.mplot3d import Axes3D

rcParams["text.usetex"] = True
rcParams["font.monospace"] = "Computer Modern Typewriter"

def big_plot(title="", fontsize=12, threeD=False):
    if threeD:
        fig = plt.figure()
        ax = plt.axes(projection='3d')
    else:
        fig, ax = plt.subplots(1,1) 
    fig.set_size_inches(11,8.5)
    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=3.0)
    fig.suptitle(title, fontsize=fontsize)
    return fig, ax

def velocity_comps_2D(x,y,u,v,gridsize=10):
    ##Plots u and v velocity components for final timestep against y poisition
    plot_title = (r"Plot of $\tilde{u}(\tilde{x}=0.05,y)$ and $\tilde{v}(\tilde{x}=0.05,y)$" 
        r" for $0 \leq y \leq 0.1$ with a grid size of "  + str(gridsize)+"x"+str(gridsize))

    fig, ax = big_plot(plot_title)
    ax.scatter(y, u, label=r"$\tilde{u}(\tilde{x}=0.5,y)$")
    ax.scatter(y, v, label=r"$\tilde{v}(\tilde{x}=0.5,y)$")
    ax.set_xlabel(r"Position on $\tilde{y}$ axis (m)")
    ax.set_ylabel(r"Velocity (m/s)")
    ax.legend()
    fig.savefig("VeloPlot_" + str(gridsize) + "grid.png")

def velocity_comps_2D_times(x,y,u,v,t,gridsize=10):
    ##Plots u and v velocity components in every timestep against y position
    ##Final vizualization definitely needs work

    plot_title = (r"Plot of $\tilde{u}(\tilde{x}=0.05,y)$ and $\tilde{v}(\tilde{x}=0.05,y)$" 
        r" for $0 \leq y \leq 0.1$ with a grid size of "  + str(gridsize)+"x"+str(gridsize) + " over all timesteps")

    fig, ax = big_plot(plot_title,threeD=True)

    ax.plot3D(y, u, t, label=r"$\tilde{u}(\tilde{x}=0.5,y)$")
    ax.plot3D(y, v, t, label=r"$\tilde{v}(\tilde{x}=0.5,y)$")
    ax.set_xlabel(r"Position on $\tilde{y}$ axis (m)")
    ax.set_ylabel(r"Velocity (m/s)")
    ax.legend()
    fig.savefig("VeloPlot_" + str(gridsize) + "grid.png")

def clocktime_vs_gridsize(gridsizes, clocktimes):
    plot_title = (r"C vs. N")
    fig, ax = big_plot(plot_title)
    gridsizes = [num ** 2 for num in gridsizes]

    ax.loglog(clocktimes, gridsizes)
    ax.set_xlabel(r"Wallclock Time (seconds)")
    ax.set_ylabel(r"Number of Grid Points")
    fig.savefig("ClocktimeVGridsize.png")