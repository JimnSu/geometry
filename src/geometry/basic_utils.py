#from numpy import (cos, sin, sqrt, pi, zeros, array, eye, empty, clip) #@UnusedImport
#from numpy import (dot, degrees, arccos, argmax, #@UnusedImport
#                   vstack, hstack, sign, #@UnusedImport
#                   ndarray, radians, float32, float64, arctan2, argmin)#@UnusedImport
#from numpy.random import uniform #@UnusedImport
#import numpy as np #@UnusedImport
#from numpy.linalg import norm #@UnusedImport
#
#from numpy.core.numeric import allclose
#
#from numpy.linalg import  det, svd  # @UnusedImport
from . import GeometryConstants, contract, np, new_contract
import warnings

new_contract('R1', 'array[1]')
new_contract('R2', 'array[2]')
new_contract('R3', 'array[3]')

@contract(s='array')
def normalize_length(s, norm=2):
    ''' Normalize an array such that it has unit length in the given norm. '''
    sn = np.linalg.norm(s, norm)
    if np.allclose(sn, 0, atol=GeometryConstants.atol_zero_norm):
        raise ValueError('Norm is zero')
    else:
        return s / sn


@contract(s='array')
def normalize_length_or_zero(s, norm=2):
    ''' 
        Normalize an array such that it has unit length in the given norm; 
        if the norm is close to zero, the zero vector is returned.     
    '''
    sn = np.linalg.norm(s, norm)
    if np.allclose(sn, 0, atol=GeometryConstants.atol_zero_norm):
        return s
    else:
        return s / sn


@new_contract
@contract(x='array')
def finite(x):
    # TODO: make into standard thing
    return np.isfinite(x).all()


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    def new_func(*args, **kwargs):
        # TODO: mofify stack
        warnings.warn("Call to deprecated function %s." % func.__name__,
                      category=DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


def safe_arccos(x):
    ''' 
        Returns the arcosine of x, clipped between -1 and 1.
        
        Use this when you know x is a cosine, but it might be
        slightly over 1 or below -1 due to numerical errors.
    '''
    return np.arccos(np.clip(x, -1.0, 1.0))
