import unittest

import numpy as np

from snp_geometry import random_rotation, random_quaternion, random_direction, \
    geodesic_distance_on_S2, \
     random_directions, assert_allclose
     
from contracts import check, fail


N = 20

class GeometryTests(unittest.TestCase):
    
    # TODO: add statistics test
    def test_random_quaternions(self):
        for i in range(N): #@UnusedVariable
            random_quaternion()
        
    def test_random_rotations(self):
        for i in range(N): #@UnusedVariable
            random_rotation()
    
    def test_random_direction(self):
        for i in range(N): #@UnusedVariable
            random_direction()
        
    def test_checks(self):
        R = np.zeros((10, 10))
        fail('rotation_matrix', R)
        R = random_rotation()
        R[0, 2] += R[0, 1]
        fail('rotation_matrix', R)

        R = random_rotation()
        R *= 2
        fail('rotation_matrix', R)

    def test_unit_length(self):
        
        check('unit_length', np.array([1]))
        check('unit_length', np.array([0, 1]))
        fail('unit_length', np.array([0, 2]))
        
    def test_random_directions(self):
        N = 20
        x = random_directions(N)
        assert x.shape == (3, N)
        
    def test_distances(self):
        for i in range(N): #@UnusedVariable
            s = random_direction()
            dist = geodesic_distance_on_S2 
            assert_allclose(dist(s, s), 0)
            assert_allclose(dist(s, -s), np.pi)
