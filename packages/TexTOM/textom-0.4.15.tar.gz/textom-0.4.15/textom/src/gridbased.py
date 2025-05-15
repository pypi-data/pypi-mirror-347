import numpy as np
from numba import njit

from . import rotation as rot
from ..config import data_type

@njit
def fisher_SO3(Q, q_mu, kappa, Q_gen, dV): 
    """
    von Mises-Fisher distribution on fundamental zone (fz)

    Parameters
    --------
    Q : 2d ndarray, float
        array of unit quaternions representing orientations
    mu: 1d ndarray, float 
        mean orientation as quaternion
    kappa: float
        concentration parameter for von Mises-Fisher distribution (~1/sigma^2) ! this seems not correct
    gen: 2d ndarray, float
        OTP of the two generators for the point group symmetries
        dim0: generators, dim1: OTP
    dV: 1d ndarray, float
        Volume element in SO(3) for each orientation in g
        important for non-cubochoric sampling
    
    Returns:
    ------------
    odf: 1d ndarray, float
        non-normalized probabilty (mass) for each of the orientations g
    """

    # !!!!!!!! working well for most q_mu but for some it fails !!!!!!!!!!!!!

    # We put multiple (mises-fisher) bell functions on the unit quaternion sphere
    # One on every symmetry equivalent q_mu
    # Evaluate the sum of these on orientations Q
    q_mu_equivalents = symmetry_equivalents_around_fz(q_mu,Q_gen)
    # q_mu_equivalents = np.atleast_2d(q_mu) # this is to show what happens if you use only q_mu

    # calculate odf as a sum of distributions from equivalents
    odf = np.zeros((q_mu_equivalents.shape[0],Q.shape[0]), dtype=data_type)
    for i in range(q_mu_equivalents.shape[0]):
        mux = np.abs( q_mu_equivalents[i] @ Q.T )
        odf[i]= np.exp(mux * kappa)
    odf = np.sum(odf, axis=0)# / np.exp(kappa)
    return odf / odf.max()

@njit
def gaussian_3d( Q, q_mu, std, gen, dV=1 ):
    """
    Gauss bell on FZ
    Parameters
    --------
    Q : 2d ndarray, float
        array of unit quaternions representing orientations
    mu: 1d ndarray, float 
        mean orientation as quaternion
    std: float
        standard deviation - sigma
    gen: 2d ndarray, float
        OTP of the two generators for the point group symmetries
        dim0: generators, dim1: OTP
    
    Returns:
    ------------
    odf: 1d ndarray, float
        non-normalized probabilty (mass) for each of the orientations g
    """
    # for omega_mu = 0, then dg is omega
    dg = rot.ang_distance(Q, nb_full(Q.shape,q_mu), gen)
    odf = np.exp( - dg**2/(2*std**2) )
    return odf #/( odf @ dV ) Does not return a valid pmf at the moment

@njit
def symmetry_equivalents_around_fz(q, Q_gen, prec=5):
    Q_gen_rev = Q_gen.copy()
    Q_gen_rev[:,1:] *= -1

    # get all symmetry-equivalents to q
    Q_eq = np.empty((13,4),data_type)
    q_0forth = rot.q_mult(Q_gen[0], q)
    q_0back = rot.q_mult(Q_gen_rev[0], q)
    q_1forth = rot.q_mult(Q_gen[1], q)
    q_1back = rot.q_mult(Q_gen_rev[1], q)
    Q_eq[0] = q
    Q_eq[1] = q_0forth
    Q_eq[2] = q_0back
    Q_eq[3] = q_1forth
    Q_eq[4] = q_1forth
    Q_eq[5] = rot.q_mult(Q_gen[1], q_0forth)
    Q_eq[6] = rot.q_mult(Q_gen[1], q_0back)
    Q_eq[7] = rot.q_mult(Q_gen[0], q_1forth)
    Q_eq[8] = rot.q_mult(Q_gen[0], q_1back)
    Q_eq[9] = rot.q_mult(Q_gen_rev[1], q_0forth)
    Q_eq[10] = rot.q_mult(Q_gen_rev[1], q_0back)
    Q_eq[11] = rot.q_mult(Q_gen_rev[0], q_1forth)
    Q_eq[12] = rot.q_mult(Q_gen_rev[0], q_1back)
        
    Q_eq[Q_eq[:,0] < 0] *= -1
    Q_eq = np.round(Q_eq, prec)
    Q_eq = nb_unique_axis0(Q_eq)
    # np.round( np.array([
    #     q,
    #     q_0forth,
    #     q_0back,
    #     q_1forth,
    #     q_1forth,
    #     rot.q_mult(Q_gen[1], q_0forth),
    #     rot.q_mult(Q_gen[1], q_0back),
    #     rot.q_mult(Q_gen[0], q_1forth),
    #     rot.q_mult(Q_gen[0], q_1back),
    #     rot.q_mult(Q_gen_rev[1], q_0forth),
    #     rot.q_mult(Q_gen_rev[1], q_0back),
    #     rot.q_mult(Q_gen_rev[0], q_1forth),
    #     rot.q_mult(Q_gen_rev[0], q_1back),
    #     ],data_type), prec)
    return Q_eq

from .misc import integrate_c
from numba import prange
# @njit(parallel=True)
def projection( g, Qc, Isc, gen, Q_mu, c_sample, kappa, Qs, Beams, iBeams, detShape, dV ):
    diff_patterns_g = np.empty((Beams.shape[1],detShape[0],detShape[1]), data_type)
    for t in prange(Beams.shape[1]):
        # project the coefficients
        iend = np.searchsorted(iBeams[g,t,:],2**32-1) # for sparsearray
        c_proj = integrate_c( Beams[g,t,:iend], iBeams[g,t,:iend], c_sample )
        # get the resulting odf from rotated mu
        odf_proj = np.zeros( Qc.shape[0], data_type )
        idcs_basis = np.nonzero(c_proj > 0.01 * c_proj.max())[0]
        for c in idcs_basis:
            q_mu = rot.q_mult(  Q_mu[c], Qs[g] )
            odf_proj += c_proj[c] * fisher_SO3(Qc, q_mu, kappa, gen, dV )
        # sparse calculate the projections (only points in odf that are high)
        diff_pattern = np.zeros(Isc.shape[1], data_type)
        idcs_odf = np.nonzero(odf_proj> 0.01 * odf_proj.max())[0]
        for h in idcs_odf:
            diff_pattern += Isc[h] * odf_proj[h]
        diff_patterns_g[t] = diff_pattern.reshape((detShape[0],detShape[1]))
    return diff_patterns_g

@njit
def nb_full(shape, fill_array):
    out = np.empty((shape[0], fill_array.shape[0]), dtype=fill_array.dtype)
    for i in range(shape[0]):
        for j in range(fill_array.shape[0]):
            out[i, j] = fill_array[j]
    return out

@njit
def nb_unique_axis0(arr):
    n, m = arr.shape
    output = np.empty((n, m), dtype=arr.dtype)
    count = 0

    for i in range(n):
        duplicate = False
        for j in range(count):
            is_same = True
            for k in range(m):
                if arr[i, k] != output[j, k]:
                    is_same = False
                    break
            if is_same:
                duplicate = True
                break
        if not duplicate:
            for k in range(m):
                output[count, k] = arr[i, k]
            count += 1

    return output[:count]