from . import np, MatrixLieAlgebra, so, contract
from .. import extract_pieces, combine_pieces, hat_map_2d, hat_map


class se_algebra(MatrixLieAlgebra):
    ''' This is the Lie algebra se(n) for the Special Euclidean group SE(n). 
    
        Note that you have to supply a coefficient *alpha* that
        weights rotation and translation when defining distances. 
    '''

    def __init__(self, N, alpha):
        dimension = {2: 3, 3: 6}[N]
        MatrixLieAlgebra.__init__(self, n=N + 1, dimension=dimension)
        self.alpha = alpha
        self.son = so[N]

    def norm(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        return np.linalg.norm(v) + self.alpha * self.son.norm(W)

    def project(self, X):
        W, v, zero, zero = extract_pieces(X) #@UnusedVariable
        W = self.son.project(W)
        return combine_pieces(W, v, v * 0, 0)

    def __repr__(self):
        #return 'se(%s)' % (self.n - 1)
        return 'se%s' % (self.n - 1)

    @contract(a='belongs')
    def vector_from_algebra(self, a):
        """ Note that it returns (omega, vx, vy) or (w1,w2,w3,vx,vy,vz) """
        W, v, zero, zero = extract_pieces(a) #@UnusedVariable

        if self.n == 3:
            assert v.size == 2
            V = np.zeros(3)
            V[0] = self.son.vector_from_algebra(W)
            V[1:3] = v
            return V
        elif self.n == 4:
            assert v.size == 3
            V = np.zeros(6)
            V[0:3] = self.son.vector_from_algebra(W)
            V[3:6] = v
            return V
        else:
            assert False, 'Not implemented for n>=4.'

    @contract(v='array[N]', returns='belongs')
    def algebra_from_vector(self, v):
        """ Note that the first element is (omega, vx, vy) or 
            (w1,w2,w3,vx,vy,vz) """

        if self.n == 3:
            assert v.size == 3
            omega = v[0]
            vel = v[1:3]
            W = hat_map_2d(omega)
            return combine_pieces(W, vel, vel * 0, 0)

        elif self.n == 4:
            assert v.size == 6
            omega = v[0:3]
            vel = v[3:6]
            W = hat_map(omega)
            return combine_pieces(W, vel, vel * 0, 0)
        else:
            assert False, 'Not implemented for n=%d.' % self.n

    def interesting_points(self):
        points = []
        points.append(self.zero())
        if self.n == 3:
            from . import SE2
            points.extend([SE2.algebra_from_group(p)
                           for p in SE2.interesting_points()])
        elif self.n == 4:
            from . import SE3
            points.extend([SE3.algebra_from_group(p)
                           for p in SE3.interesting_points()])
        else:
            assert False, 'Not implemented for n=%s' % self.n
        return points