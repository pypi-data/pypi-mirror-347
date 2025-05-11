import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def binding_vectors_from_bedpe(bedpe_file,N_beads,region,chrom,normalization=False,viz=False):
    '''
    Definition of left and right CTCF binding potential.

    Input:
    bedpe_file (str): path with bepde file with loops
    region (list): a list with two integers [start,end], which represent the start and end point of the region of interest.
    chrom (str): chromosome of interest.
    normalization (bool): in case that it is needed to normalize to numpy arrays that represent left and right CTCF binding potential.
    viz (bool): If True is vizualizes the distribution of distances of loops from the diagonal and the binding potentials as functions of simulated polymer distance.

    Output:
    L (numpy array): left CTCF binding potential.
    R (numpy array): right CTCF binding potential.
    dists (numpy array): distances of CTCF loops from the diagonal.
    '''
    # Read file and select the region of interest
    df = pd.read_csv(bedpe_file,sep='\t',header=None)
    df = df[(df[1]>=region[0])&(df[2]>=region[0])&(df[4]>=region[0])&(df[5]>=region[0])&(df[5]<region[1])&(df[4]<region[1])&(df[1]<region[1])&(df[2]<region[1])&(df[0]==chrom)].reset_index(drop=True)

    # Convert hic coords into simulation beads
    resolution = (region[1]-region[0])//N_beads
    df[1], df[2], df[4], df[5] = (df[1]-region[0])//resolution, (df[2]-region[0])//resolution, (df[4]-region[0])//resolution, (df[5]-region[0])//resolution
    
    # Check if columns 7 and 8 exist
    has_col_7_8 = df.shape[1] > 8
    if has_col_7_8:
        print("\033[92mThe input bedpe file contains CTCF orientation! It will run taking it into account.\033[0m")
    else:
        print("\033[93mWARNING: The input bedpe file does not contain CTCF orientation and thus it is not taken into account. If you would like to add CTCF orientation check the documentation.\033[0m")

    # Compute the matrix
    distances = list()
    J = np.zeros((N_beads,N_beads), dtype=np.float64)
    L, R = np.zeros(N_beads, dtype=np.float64),np.zeros(N_beads, dtype=np.float64)
    for i in range(len(df)):
        x, y = min((df[1][i]+df[2][i])//2,N_beads-1), min((df[4][i]+df[5][i])//2,N_beads-1)
        distances.append(distance_point_line(x,y))
        J[x,y] = 0
        J[y,x] = 0
        if has_col_7_8:
            if df[7][i]>=0: L[x] += df[6][i]*(1-df[7][i])
            if df[8][i]>=0: L[y] += df[6][i]*(1-df[8][i])
            if df[7][i]>=0: R[x] += df[6][i]*df[7][i]
            if df[8][i]>=0: R[y] += df[6][i]*df[8][i]
        else:
            L[x] += df[6][i]
            L[y] += df[6][i]
            R[x] += df[6][i]
            R[y] += df[6][i]
    
    # Normalize (if neccesary): it means to convert values to probabilities
    if normalization:
        L, R = L/np.sum(L), R/np.sum(R)

    if viz:
        fig, axs = plt.subplots(2, figsize=(15, 10))
        axs[0].plot(L,'g-')
        axs[0].set_ylabel('Left potential',fontsize=16)
        axs[1].plot(R,'r-')
        axs[1].set_ylabel('Right potential',fontsize=16)
        axs[1].set_xlabel('Genomic Distance (with simumation beads as a unit)',fontsize=16)
        fig.show()

    return L, R, J

def distance_point_line(x0,y0,a=1,b=-1,c=0):
    return np.abs(a*x0+b*y0+c)/np.sqrt(a**2+b**2)