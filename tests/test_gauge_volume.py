import numpy as np
import unittest
from numpy.testing import assert_allclose
from c3dp.gaugevol import gauge_volume as gv


class TestGaugeVolume(object):
    def test_make_square(self):
        collimator_inner_radius=16.02
        collimator_openningSize_sample=3.
        Cs_square = gv.make_square(collimator_inner_radius, collimator_openningSize_sample)
        reference=[[16.02, -3./2, 3./2], [16.02, 3./2, 3./2], [16.02, 3./2, -3./2], [16.02, -3./2, -3./2]]
        assert_allclose(Cs_square, reference)

    def test_theta_phi(self):
        Cs_square = [[16.02, -3./2, 3./2], [16.02, 3./2, 3./2], [16.02, 3./2, -3./2], [16.02, -3./2, -3./2]] # four points in the square of collimator openning at sample side
        sample_points=np.array([(0.,3.), (0.,2.), (0.,5.)]).T  #two points of the sample (0,0,0) (3,2,5)

        reference_s=(np.array([[-1.47743557, -1.66415709, -1.66415709, -1.47743557],
       [-1.30818725, -1.53241273, -1.53241273, -1.30818725]]), np.array([[ 1.66375285,  1.66375285,  1.47783981,  1.47783981],
       [ 1.31680198,  1.30837191,  1.10805774,  1.1215578 ]])) # phi of four points of collimator openning at sample side
                                                                                                                        # from two points in sample

        theta_phiS = gv.theta_phi(Cs_square, sample_points)

        assert_allclose(theta_phiS, reference_s)

        Cd_square = [[396.02, -74.16/ 2, 74.16/ 2], [396.02, 74.16/ 2, 74.16/ 2], [396.02, 74.16/2, -74.16/ 2],
                     [396.02, -74.16/ 2, -74.16/ 2]] # four points in the square of collimator openning at detector side


        theta_phid = gv.theta_phi(Cd_square, sample_points)


        reference_d=(np.array([[-1.47743688, -1.66415577, -1.66415577, -1.47743688],
       [-1.47168697, -1.65981796, -1.65981796, -1.47168697]]), np.array([[ 1.66375155,  1.66375155,  1.4778411 ,  1.4778411 ],
       [ 1.6518422 ,  1.65191903,  1.46455351,  1.46465382]])) # phi of four points of collimator openning at detector side
                                                                                                                        # from two points in sample

        assert_allclose(theta_phid, reference_d)




    def test_gauge_volume(self):

        theta_phiS= (np.array([[-1.47743557, -1.66415709, -1.66415709, -1.47743557],
       [-1.30818725, -1.53241273, -1.53241273, -1.30818725]]), np.array([[ 1.66375285,  1.66375285,  1.47783981,  1.47783981],
       [ 1.31680198,  1.30837191,  1.10805774,  1.1215578 ]]))  # phi of four points of collimator openning at sample side
                                                                                                                        # from two points in sample

        theta_phiD = (np.array([[-1.47743688, -1.66415577, -1.66415577, -1.47743688],
       [-1.47168697, -1.65981796, -1.65981796, -1.47168697]]), np.array([[ 1.66375155,  1.66375155,  1.4778411 ,  1.4778411 ],
       [ 1.6518422 ,  1.65191903,  1.46455351,  1.46465382]]))# phi of four points of collimator openning at detector side
                                                                                                                        # from two points in sample

        Syz = np.array([ (0.,2.), (0.,5.) ]) # (y,z) in sample for two points

        sample_pos, gauge_volume = gv.gauge_volume(theta_phiS, theta_phiD, Syz)

        reference_gauge_volume=[1] #non zero gauge volume
        reference_sample_pos=np.array([0,0]).reshape(2,1) #(y,z) for corresponding positon in sample for non_zero gauge volume

        assert_allclose(sample_pos, reference_sample_pos)
        assert_allclose(gauge_volume, reference_gauge_volume)

    @unittest.skip("skipping the plot")
    def test_making_plot(self):
        sample_pos=np.array([ [0.,2.], [0.,5.] ])

        gauge_volume = [1, 0]

        gv.making_plot(sample_pos, gauge_volume, -2,2 )

    if __name__ == '__main__':
        unittest.main()













