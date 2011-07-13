from . import np, DifferentiableManifold, contract
from contracts import check
from abc import abstractmethod
from geometry.basic_utils import assert_allclose
from geometry.formatting import formatm, printm

class MatrixLinearSpace(DifferentiableManifold):
    
    @contract(dimension='int,>0')
    def __init__(self, dimension, shape):
        ''' Note dimension is the intrinsic dimension. '''
        # TODO: give basis?
        self.shape = shape
        DifferentiableManifold.__init__(self, dimension=dimension)

    def zero(self):
        ''' Returns the zero element for this algebra. '''
        return np.zeros(self.shape)

    def norm(self, v):
        ''' Return the norm of a vector in the algebra.
            This is used in :py:class:`MatrixLieGroup` to measure
            distances between points in the Lie group. 
        '''
        return np.linalg.norm(v, 2)
    
    # Manifolds methods
    def distance(self, a, b):
        return self.norm(a - b)
    
    @contract(bv='belongs_ts')
    def expmap(self, bv):
        base, vel = bv
        return base + vel
        
    @contract(base='belongs', target='belongs', returns='belongs_ts')
    def logmap(self, base, target):
        return base, target - base
        
    def belongs(self, x):
        check('shape(x)', x, x=self.shape)
        assert np.all(np.isreal(x)), "Expected real vector" # TODO: make contract
        proj = self.project(x)
        assert_allclose(proj, x, atol=1e-8) # XXX: tol
        
    def belongs_ts(self, bv):
#        formatm('bv', bv)
        check('tuple(shape(x),shape(x))', bv, x=self.shape)
        base, vel = bv
        self.belongs(base)
        self.belongs(vel)
     
    @abstractmethod        
    def project(self, v): #@UnusedVariable
        ''' Projects a vector onto this Lie Algebra. '''
        
        
    def project_ts(self, bv):
        base, vel = bv
        return base, self.project(vel)