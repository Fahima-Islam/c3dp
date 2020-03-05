from c3dp.instrument.collimator.section import CollimatorSection, blade_configurations
import numpy as np
from collections import namedtuple
import pytest


class TestCollimatorSection(object):
    def test_n_blades_from_thickness(self):
        small_section = CollimatorSection(12, 50, 10)
        np.testing.assert_allclose(small_section.n_blades_from_thickness(3), 1, atol=0.01)

    def test_channel_thickness(self):
        small_section = CollimatorSection(12, 50, 10)
        np.testing.assert_allclose(small_section.chanel_thickness(10), 0.0, atol=0.01)

    def test_set_blade_angles(self):
        small_section = CollimatorSection(12, 50, 10)
        np.testing.assert_allclose(max(small_section.set_blade_angles(10)), 0.0, atol=0.01)

    def test_blade_blade_angle_distances(self):
        small_section = CollimatorSection(12, 50, 10)
        np.testing.assert_allclose(small_section.blade_blade_angle_distances(np.array([[4, 3], [4, 3]])),
                                   0.0, atol=0.01)

    Triad = namedtuple('Triad', 'blades d widths')

    @pytest.mark.parametrize('expected', [Triad([1, 2, 1], 10.47, [6.80, 19.88, 53.62])])
    def test_blade_configurations(self, expected):
        np.testing.assert_allclose(blade_configurations(20, 60, 45)[0][0], expected[0], atol=0.01)
