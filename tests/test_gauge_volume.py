import numpy as np

import unittest

from c3dp import gauge_volume as gv


sample_height=26. #mm
sample_width=4.16 #mm
collimator_thickness_sample=3. # channel opening size
collimator_inner_radius=16.02
coll_length=380.
collimator_outer_radius=coll_length+collimator_inner_radius
collimator_thickness_detector=(collimator_outer_radius*collimator_thickness_sample)/collimator_inner_radius

pointsNum=5
zS=np.linspace(-sample_height/2., sample_height/2., num=pointsNum) #sample_positions_z vertical
yS=np.linspace(-sample_width/2., sample_width/2., num=pointsNum) #saNoNsymmetric_Resolution_Test1mple_positions_y
xS=np.linspace(-sample_width/2., sample_width/2., num=pointsNum) #sample_positions_x
Sxy = np.array([xS, yS])
S = np.array([xS, yS, zS]).T



class TestGaugeVolume(object):
    def test_make_square(self):
        Cs_square = gv.make_square(collimator_inner_radius, collimator_thickness_sample)
        Cd_square = gv.make_square(collimator_outer_radius, collimator_thickness_detector)



    def test_theta_phi(self):
        Cs_square = gv.make_square(collimator_inner_radius, collimator_thickness_sample)
        Cd_square = gv.make_square(collimator_outer_radius, collimator_thickness_detector)
        sample_points=S

        theta_phiS = gv.theta_phi(Cs_square, sample_points)
        theta_phiD = gv.theta_phi(Cd_square, S)

    def test_gauge_volume(self):
        Cs_square = gv.make_square(collimator_inner_radius, collimator_thickness_sample)
        Cd_square = gv.make_square(collimator_outer_radius, collimator_thickness_detector)
        sample_points = S

        theta_phiS = gv.theta_phi(Cs_square, sample_points)
        theta_phiD = gv.theta_phi(Cd_square, S)
        gauge_volume = gv.gauge_volume(theta_phiS, theta_phiD)


    def test_making_plot(self):
        Cs_square = gv.make_square(collimator_inner_radius, collimator_thickness_sample)
        Cd_square = gv.make_square(collimator_outer_radius, collimator_thickness_detector)
        sample_points = S

        theta_phiS = gv.theta_phi(Cs_square, sample_points)
        theta_phiD = gv.theta_phi(Cd_square, S)
        gauge_volume = gv.gauge_volume(theta_phiS, theta_phiD)
        gv.making_plot(Sxy, gauge_volume )

    if __name__ == '__main__':

        unittest.main()













