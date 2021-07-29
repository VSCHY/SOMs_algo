import matplotlib.pyplot as plt
import numpy as np

def kohonen_map(xdim, ydim, data, outdir):
    # Plot Kohonen map : nb of element per cluster
    plt.figure()
    plt.pcolor(np.arange(0,xdim+1),np.arange(0,xdim+1), data)
    plt.xlabel("m")
    plt.xlim((0,xdim))
    plt.ylim((0,ydim))
    plt.xticks(np.arange(0.5,xdim), np.arange(1,xdim+1))
    plt.yticks(np.arange(0.5,ydim), np.arange(1,ydim+1))
    plt.ylabel("n")
    plt.colorbar()
    plt.title("Kohonen Map")
    plt.savefig(outdir, dpi = 300)
