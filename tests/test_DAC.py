from c3dp.instrument.cellgeometry.DAC_geo import DAC
import numpy as np


class Test_DAC_properties(object):
    def __init__(self):
        self.dac = DAC()

    def test_angle2span(self):
        np.testing.assert_allclose(self.dac.angle2span(10, 45), 10, atol=0.01)

    def test_span2angle(self):
        np.testing.assert_allclose(self.dac.span2angle(10, 20), 20, atol=0.01)

    def test_size_at_sample_side(self):
        np.testing.assert_allclose(self.dac.size_at_sample_side(20, 13, 10), 20, atol=0.01)

    def test_crown_top_triangle_height(self):
        np.testing.assert_allclose(self.dac.crown_top_triangle_height(), 0.1, atol=0.01)

    def test_pavilion_bottom_triangle_height(self):
        np.testing.assert_allclose(self.dac.pavilion_bottom_triangle_height(), 10, atol=0.01)
