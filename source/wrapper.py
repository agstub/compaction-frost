# these functions are used for running simulations over a range of parameters 
# in parallel with ipyparallel
from solvers import time_stepping, initialize
from dolfinx.mesh import create_interval
from mpi4py import MPI
from params import nz
import numpy as np


def wrapper_v(i,v_i,z_0):
    # wrapper for varying v_i across simulations for parallel
    # computing with ipyparallel
    N_f = 2.0  # effective stress at base of fringe 
    timesteps = np.linspace(0,1e3,1000)
    z_l0 = z_0[i]
    z_b = 1e-3
    gamma = 0
    N_c = 0.05
    const_phi = False
    domain = create_interval(MPI.COMM_WORLD,nz,[z_b,z_l0])
    initial = initialize(domain,N_f,gamma,const_phi,eps_min=1e-10)
    N, heave, visc, z, new_lens, converged = time_stepping(domain,initial,N_f,N_c,gamma,const_phi,v_i,timesteps,eps=1e-10,break_init = True)
    z_l = z[:,-1]
    return([z_l,new_lens,[converged]])


def wrapper_N(i,N_f,v_i,timesteps):
    # wrapper for varying N_f across simulations for parallel
    # computing with ipyparallel
    z_l = 5
    z_b = 1e-3
    domain = create_interval(MPI.COMM_WORLD,nz,[z_b,z_l])
    gamma = 0
    const_phi = False
    N_c = 0.05
    initial = initialize(domain,N_f,gamma,const_phi,eps_min=1e-10)
    N, heave, visc, z, new_lens, converged = time_stepping(domain,initial,N_f,N_c,gamma,const_phi,v_i[i],timesteps,eps=1e-10)
    z_l = z[:,-1]
    return([z_l,new_lens])

def wrapper_gamma(i,timesteps,v_i,gamma):
    # wrapper for varying gamma=lambda^2 across simulations for parallel
    # computing with ipyparallel
    N_f = 2.0
    z_l = 5
    z_b = 1e-3
    domain = create_interval(MPI.COMM_WORLD,nz,[z_b,z_l])
    const_phi = False
    N_c = 0.05
    initial = initialize(domain,N_f,gamma[i],const_phi,eps_min=1e-10)
    N, heave, visc, z, new_lens, converged = time_stepping(domain,initial,N_f,N_c,gamma[i],const_phi,v_i,timesteps,eps=1e-10)
    z_l = z[:,-1]
    return([z_l,new_lens])    